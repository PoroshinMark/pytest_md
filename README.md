# pytest-md

A pytest plugin for generating beautiful Markdown test reports with detailed test information, metadata, and execution statistics.

## Features

- 📊 **Comprehensive Test Reports**: Generate detailed Markdown reports with test outcomes, durations, and metadata
- 🎯 **Test Outcome Tracking**: Track passed, failed, skipped, errors, expected failures, and unexpected passes
- 📝 **Custom Metadata**: Add custom information to tests using the `extras` fixture
- ⏱️ **Duration Tracking**: Monitor test execution times and total session duration
- 📋 **Detailed Logs**: Capture and display test logs and output
- 🎨 **Beautiful Formatting**: Clean, readable Markdown output with emojis and structured sections
- 🔧 **Easy Integration**: Simple command-line interface with minimal configuration

## Installation

### From Source

```bash
git clone <repository-url>
cd pytest-md
pip install -e .
```

### Dependencies

- Python 3.12+
- pytest >= 8.4.1
- jinja2 >= 3.1.6

## Usage

### Basic Usage

Generate a Markdown report for your test suite:

```bash
pytest --md=report.md tests/
```

### Configuration

You can configure the plugin in your `pytest.ini` or `pyproject.toml`:

```ini
[tool:pytest]
addopts = --md=report.md
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Adding Custom Metadata

Use the `extras` fixture to add custom information to your tests:

```python
import pytest

def test_example(extras):
    extras.append("Custom metadata")
    extras.append("Additional information")
    assert True
```

## Example Output

The plugin generates a comprehensive Markdown report with the following sections:

### Executive Summary
- Total test count and execution status
- Overall duration

### Test Outcomes
- Breakdown of test results by outcome type
- Percentage distribution
- Visual indicators (emojis) for different outcomes

### Detailed Test Results
- Individual test information
- Custom metadata from the `extras` fixture
- Test logs and captured output
- Duration for each test

## Report Structure

```
# Test Report

## 📊 Executive Summary
| **Total Tests** | **Status** | **Duration** |
|:---------------:|:----------:|:------------:|
| 2 tests took 1 ms. | finished | 0.00s |

## 🎯 Test Outcomes
| Outcome | Count | Percentage |
|:--------|:-----:|:----------:|
| ✅ **Passed** | 2 | 100.0% |
| ❌ **Failed** | 0 | 0.0% |

## 🧪 Detailed Test Results
### ✅ Test: tests/test_example.py::test_function
**Status:** 🟢 **PASSED**
**Duration:** ⏱️ 0.000s

#### 📝 Metadata
Custom metadata
Additional information

#### 📋 Logs
<details>
<summary>📄 Click to view logs</summary>
```bash
No log output captured.
```
</details>
```

## Development

### Project Structure

```
pytest_md/
├── __init__.py          # Plugin initialization
├── plugin.py            # Main plugin logic
├── report.py            # Report generation
├── report_data.py       # Data management
├── fixtures.py          # Custom fixtures
├── utils.py             # Utility functions
└── res/
    └── report.template.jinja2  # Report template
```

### Running Tests

```bash
# Run tests with the plugin
pytest --md=report.md tests/

# Run tests with verbose output
pytest --md=report.md tests/ -v

# Run specific test file
pytest --md=report.md tests/test_specific.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the Mozilla Public License 2.0.

## Changelog

### 0.1.0
- Initial release
- Basic Markdown report generation
- Support for custom metadata via `extras` fixture
- Comprehensive test outcome tracking
- Beautiful formatting with emojis and structured sections
