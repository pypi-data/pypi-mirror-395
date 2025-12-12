# Pmini SDK Python


## Get started

```bash
python -m venv venv
```


```bash
source venv/bin/activate
```

```
poetry build
```

```
pip install ./dist/pmini-0.0.0-py3-none-any.whl --force-reinstall
```

## Examples

After installing the package, go to the examples folder and run any of the examples

```
cd examples
```

Run example

```
python3 takeoff.py
```


# Integration Tests for Pmini SDK

This directory contains integration tests for the Pmini SDK Python library.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_basic.py` - Basic tests that don't require simulation
- `test_connection.py` - Connection tests that require simulation
- `run_integration_tests.py` - Test runner script

## Prerequisites

1. Install dependencies:

```bash
pip install pytest pytest-cov
```

2. Install the SDK:
```bash
pip install -e .
```

## Running Tests

### Note 

For the integration testing, autopilot simulation is required.
You can use this repository to start the simulation: https://gitlab.com/regislab/pathfindermini/pf_mini_gazebo

```bash
git clone git@gitlab.com:regislab/pathfindermini/pf_mini_gazebo.git && cd pf_mini_gazebo
```

Launch the simulation with the following command

```bash
make run
```

### Basic Tests (No Simulation Required)
```bash
# Run basic tests only
python -m pytest test/test_basic.py -v

# Or use the test runner
python test/run_integration_tests.py --test-path test/test_basic.py
```

### Connection Tests (Requires Simulation)
```bash
# Start your simulation container first, then:
python -m pytest test/test_connection.py -v

```

### All Tests
```bash
# Run all tests
python -m pytest test/ -v
```

### With Markers
```bash
# Run only integration tests
python -m pytest test/ -m integration

# Run only connection tests
python -m pytest test/ -m connection

# Exclude slow tests
python -m pytest test/ -m "not slow"
```

## Test Configuration

The tests are configured to connect to a simulation running on:
- Host: `192.168.4.1`
- Port: `8080`
- Protocol: `UDP`

You can modify the connection settings in `conftest.py` if your simulation uses different parameters.

## Test Categories

### Basic Tests (`test_basic.py`)
- SDK import verification
- Configuration object creation
- Enum availability
- Logging setup

### Connection Tests (`test_connection.py`)
- Connection establishment
- Connection stability
- MAVLink client functionality
- Optical flow data availability
- Connection timeout handling
- Connection recovery

## Adding New Tests

1. Create a new test file: `test_<feature>.py`
2. Use the existing fixtures from `conftest.py`
3. Add appropriate markers to your tests
4. Follow the existing test patterns

Example:
```python
import pytest
import logging

class TestNewFeature:
    @pytest.mark.integration
    def test_new_feature(self, pmini_instance, wait_for_connection):
        logger = logging.getLogger(__name__)
        logger.info("Testing new feature")
        
        # Your test logic here
        assert True
        logger.info("✅ New feature test passed")
```

## Troubleshooting

### Connection Timeout
If tests fail with connection timeout:
1. Ensure your simulation container is running
2. Check that the simulation is listening on the correct port
3. Verify network connectivity between test environment and simulation

### Import Errors
If you get import errors:
1. Make sure the SDK is installed: `pip install -e .`
2. Check that all dependencies are installed: `pip install -r requirements.txt`

### Test Failures
- Check the logs for detailed error messages
- Use `-v` flag for verbose output
- Use `-s` flag to see print statements 
