// my_extension.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <torch/extension.h>
#include <torch/csrc/distributed/c10d/ProcessGroup.hpp>
#include <thread>
#include <iostream>
#include <unistd.h>
#include <sys/time.h>
#include <time.h>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <signal.h>
#include <unistd.h> // for getpid()
#include <cstdlib>  // for getenv

namespace py = pybind11;
using namespace c10d;

// ============ Debug logging control ============
// Control log levels via environment variables:
// PG_HOOK_DEBUG=1  Enable debug logging (DEBUG level)
// PG_HOOK_INFO=0   Disable info logging (INFO level, enabled by default)
static bool g_debug_enabled = false;
static bool g_info_enabled = true;  // INFO level enabled by default

void init_log_flags() {
    const char* debug_env = std::getenv("PG_HOOK_DEBUG");
    g_debug_enabled = (debug_env != nullptr && std::string(debug_env) == "1");
    
    const char* info_env = std::getenv("PG_HOOK_INFO");
    // Only disable INFO level logging when explicitly set to "0", otherwise default to enabled
    g_info_enabled = (info_env == nullptr || std::string(info_env) != "0");
}

#define DEBUG_LOG(msg) \
    do { \
        if (g_debug_enabled) { \
            std::cout << "[DEBUG C++] " << msg << std::endl; \
        } \
    } while(0)

#define DEBUG_PRINTF(fmt, ...) \
    do { \
        if (g_debug_enabled) { \
            printf("[DEBUG C++] " fmt "\n", ##__VA_ARGS__); \
        } \
    } while(0)

#define INFO_LOG(msg) \
    do { \
        if (g_info_enabled) { \
            std::cout << "[INFO C++] " << msg << std::endl; \
        } \
    } while(0)

#define INFO_PRINTF(fmt, ...) \
    do { \
        if (g_info_enabled) { \
            printf("[C++] " fmt "\n", ##__VA_ARGS__); \
        } \
    } while(0)
// ===============================================

// Used to save work object and its enqueue time
struct TimedWork {
    py::object py_work;
    std::string op_name;
    struct timeval enqueue_tv;
    int rank;  // Add rank field
};

// Global work queue and synchronization mechanism
std::queue<TimedWork> work_queue;
std::mutex queue_mutex;
std::atomic<bool> stop_monitor(false);
std::thread monitor_thread;
std::vector<TimedWork> pending_list;        // Currently pending work (for monitoring)


void current_time(char* buf) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    time_t sec = tv.tv_sec;
    suseconds_t usec = tv.tv_usec;
    struct tm *lt = localtime(&sec);
    sprintf(buf, "%d-%02d-%02d %02d:%02d:%02d.%06d", 
            lt->tm_year + 1900,
            lt->tm_mon + 1,
            lt->tm_mday,
            lt->tm_hour,
            lt->tm_min,
            lt->tm_sec,
            (int)(usec / 1000));
}

// Calculate time difference in milliseconds
long time_diff_ms(const struct timeval& a, const struct timeval& b) {
    return (b.tv_sec - a.tv_sec) * 1000 + (b.tv_usec - a.tv_usec) / 1000;
}


void cxx_work_monitor() {
    init_log_flags();  // Initialize log flags
    DEBUG_LOG("C++ work monitor started");
    
    while (!stop_monitor) {
        // 1. Scan queue, transfer all to local pending_list
        {
            // We will be copying py::object from work_queue into pending_list.
            // Copying/holding py::object manipulates Python refcounts -> acquire GIL.
            py::gil_scoped_acquire gil;
            std::lock_guard<std::mutex> lock(queue_mutex);
            while (!work_queue.empty()) {
                pending_list.push_back(work_queue.front());
                work_queue.pop();
                DEBUG_LOG("Dequeued work from C++ queue");
            }
        }

        // 2. Traverse pending_list, check completion status
        auto it = pending_list.begin();
        while (it != pending_list.end()) {
            // Accessing py::object and py::cast requires GIL.
            py::gil_scoped_acquire gil;
            std::shared_ptr<c10d::Work> work_ptr;
            try {
                work_ptr = py::cast<std::shared_ptr<c10d::Work>>(it->py_work);
            } catch (const std::exception &e) {
                // If cast fails, remove this entry to avoid spinning on invalid object.
                DEBUG_PRINTF("Failed to cast work object: %s", e.what());
                it = pending_list.erase(it);
                continue;
            }

            // Calculate queued time
            struct timeval now;
            gettimeofday(&now, NULL);
            long elapsed = time_diff_ms(it->enqueue_tv, now);
         
            // Timeout detection: 5 minutes = 300000ms = 5 * 60 * 1000
            // Note: isCompleted() is a C++ call; it's safe to call without GIL,
            // but we currently hold the GIL. For simplicity and safety (refcount
            // on py::object until we erase), keep GIL held here.
            if (!work_ptr->isCompleted()) {
                if (elapsed > 5 * 60 *1000) { // 5 minutes in ms
                    if (it->rank >= 0) {
                        std::cout << "[C++] Rank " << it->rank << ": " << it->op_name << " timeout, sending SIGUSR1" << std::endl;
                    } else {
                        std::cout << "[C++] " << it->op_name << " timeout, sending SIGUSR1" << std::endl;
                    }
                    kill(getpid(), SIGUSR1);
                    // Optional to erase/keep pending work, depending on business needs
                    it = pending_list.erase(it);
                } else {
                    ++it;
                }
                continue;
            }
            if (work_ptr->isCompleted()) {
                // Completed, print elapsed time
                struct timeval now2;
                gettimeofday(&now2, NULL);
                long elapsed2 = time_diff_ms(it->enqueue_tv, now2);
                if (it->rank >= 0) {
                    INFO_PRINTF("Rank %d: %s complete, time: %ld ms", it->rank, it->op_name.c_str(), elapsed2);
                } else {
                    INFO_PRINTF("!!!%s complete, time: %ld ms", it->op_name.c_str(), elapsed2);
                }
                it = pending_list.erase(it);
            } else {
                ++it;
            }
        }

        // 3. Sleep for a while before polling again
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
    
    // Clean up all pending work objects before thread exits
    DEBUG_LOG("Cleaning up pending work objects...");
    {
        // Clearing containers that hold py::object requires GIL for proper refcount handling.
        py::gil_scoped_acquire gil;
        pending_list.clear();
        std::lock_guard<std::mutex> lock(queue_mutex);
        while (!work_queue.empty()) {
            work_queue.pop();
        }
    }
    
    DEBUG_LOG("C++ work monitor stopped");
}

// Start C++ monitoring thread
void start_cxx_monitor() {
    if (!monitor_thread.joinable()) {
        stop_monitor = false;
        monitor_thread = std::thread(cxx_work_monitor);
        DEBUG_LOG("C++ monitor thread started");
    }
}

// Stop C++ monitoring thread
void stop_cxx_monitor() {
    stop_monitor = true;
    if (monitor_thread.joinable()) {
        monitor_thread.join();
        DEBUG_LOG("C++ monitor thread joined");
    }
}

// Add work object to C++ queue
void enqueue_work(py::object work_py, std::string op_name, int rank) {
    TimedWork timed_work;
    timed_work.py_work = work_py;
    timed_work.op_name = op_name;
    timed_work.rank = rank;
    gettimeofday(&timed_work.enqueue_tv, NULL);

    std::lock_guard<std::mutex> lock(queue_mutex);
    work_queue.push(timed_work);
    DEBUG_PRINTF("Rank %d: Enqueued work: %s", rank, op_name.c_str());
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("start_cxx_monitor", &start_cxx_monitor,
          "Start C++ work monitoring thread");
    m.def("stop_cxx_monitor", &stop_cxx_monitor,
          "Stop C++ work monitoring thread");
    m.def("enqueue_work", &enqueue_work,
          py::arg("work_py"), py::arg("op_name"), py::arg("rank") = -1,
          "Enqueue work object to C++ monitor queue");
}