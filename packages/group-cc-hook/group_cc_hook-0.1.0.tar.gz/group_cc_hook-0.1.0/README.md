# Group Collective Communication Hook

> A monitoring solution for PyTorch distributed training that hooks into all ProcessGroup collective communication primitives and performs timeout detection in pure Python using multiprocessing to avoid GIL limitations.

## Overview

This package provides a robust monitoring mechanism for distributed PyTorch training by:

- Hooking all ProcessGroup collective communication primitives
- Implementing timeout detection using a separate process to avoid Python GIL constraints
- Sending SIGUSR1 signal when timeout is detected
- No C++ compilation required - pure Python implementation with multiprocessing

## Quick Start

### Build from Source

```bash
# Install the package (no build step needed - pure Python)
pip install .

# Run tests
torchrun --nproc_per_node=4 test_all_reduce.py 

# Test basic hook functionality
torchrun --nproc_per_node=4 test_hook_simple.py
```

### Installation

Install the package using pip:

```bash
pip install .
```

### Usage

Add the following code to your training script:

```python
from run_daemon import run_daemon, stop_daemon

# Start the monitoring daemon
run_daemon()
 
############################# Your Training Code START #########################

############################# Your Training Code END ###########################

# Stop the monitoring daemon
stop_daemon()
```

## Project Structure

```bash
├── work_monitor.py                                # Pure Python work monitoring and timeout detection
├── patch_all_collective_primi.py                  # Hooks for ProcessGroup primitives
├── run_daemon.py                                  # Daemon launcher script
├── setup.py                                       # Package setup configuration
├── test_all_reduce.py                             # AllReduce test script
├── test_hook_simple.py                            # Basic hook functionality test
├── README.md                                      # This file
└── doc/                                           # Documentation directory
    ├── DESIGN_ANALYSIS.md                         # Design analysis report
    ├── COMPATIBILITY.md                           # Version compatibility guide
    └── DEBUG_USAGE.md                             # Debug logging instructions
```

## Documentation

- [Design Analysis Report](./doc/DESIGN_ANALYSIS.md) - Comprehensive analysis of design integrity, functionality, robustness, and version compatibility
- [Version Compatibility Guide](./doc/COMPATIBILITY.md) - Compatibility information for PyTorch, Python, CUDA, and other dependencies
- [Debug Usage Guide](./doc/DEBUG_USAGE.md) - Detailed instructions for debug logging

## Requirements

- **Python**: >= 3.7, < 3.13
- **PyTorch**: >= 1.8.0, < 3.0.0
- **CUDA**: Required for GPU support (if using NCCL backend)
- **Operating System**: Linux (or any OS supporting PyTorch distributed)

For detailed compatibility information, please refer to [COMPATIBILITY.md](./doc/COMPATIBILITY.md).

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run unit tests
pytest tests/unit/

# Code quality checks
black --check .
flake8 .
```

### Contributing

Contributions are welcome! Please feel free to submit Issues and Pull Requests.

Before submitting your code, please ensure:

- All tests pass
- Code follows the project style guidelines (Black, Flake8)
- Documentation is updated if necessary

## License

See [LICENSE](./LICENSE) file for details.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and changes.
