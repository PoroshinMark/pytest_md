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
- 📈 **MLFlow Integration**: Optionally log test results to MLFlow for tracking and analysis by defining your MLFlow environment variables `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` and the fixture `metrics`

## Installation

### From PyPI (when available)

```bash
pip install pytest-md
```

### From Git

```bash
pip install git+https://github.com/PoroshinMark/pytest_md.git
```

### From Source

```bash
git clone https://github.com/PoroshinMark/pytest_md.git
cd pytest_md
pip install -e .
```

### Dependencies

- Python 3.10+
- pytest >= 8.4.1
- jinja2 >= 3.1.6

## Usage

### Basic Usage

Generate a Markdown report for your test suite:

```bash
pytest --md=report.md tests/
```

Generate a Markdown report for your test suite with MLFlow integration:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
export MLFLOW_TRACKING_USERNAME=your_username
export MLFLOW_TRACKING_PASSWORD=your_password
pytest --md=report.md --project_name=MyProject tests/
```

### Configuration

You can configure the plugin in your `pytest.ini` or `pyproject.toml`:

```ini
[tool:pytest]
addopts = --md=report.md --project_name=MyProject
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

Use the `metrics` fixture to add MLFlow metrics to your tests:

```python
import pytest

def test_example(metrics):
    metrics.append(("metric_name", 0.95))
    assert True
```

## Troubleshooting

### Template Not Found Error

If you encounter an error like:
```
jinja2.exceptions.TemplateNotFound: 'report.template.jinja2' not found
```

This usually means the package wasn't installed correctly. Try:

1. Reinstalling the package:
   ```bash
   pip uninstall pytest-md
   pip install git+https://github.com/PoroshinMark/pytest_md.git
   ```

2. Check if the template file exists in the installed package:
   ```bash
   python -c "import pytest_md; from pathlib import Path; print(Path(pytest_md.__file__).parent / 'res' / 'report.template.jinja2')"
   ```

3. If the issue persists, try installing from source instead of git.

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

## 📈 MLFlow Integration
For each test, an MLFlow experiment is created or reused based on the test identifier and the project name you provide. Additionally, a final report experiment is created with the name `"{project_name} Final Report"`.
For each experiment, the metrics you define in your tests using the `metrics` fixture will be logged to MLFlow.
For the final report, the generated Markdown report is logged as an artifact in the MLFlow experiment.

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

### 0.1.3
- Added MLFlow integration for logging test results and metrics

### 0.1.2
- Fixed HTML escaping in Jinja2 templates to allow proper rendering of HTML tags
- Disabled autoescape in template environment to support collapsible sections and other HTML content
- HTML tags like `<details>` and `<summary>` now render correctly in generated reports

### 0.1.1
- Fixed template file inclusion in package distribution
- Added fallback mechanisms for template loading
- Improved error handling for missing resources
- Added support for importlib.resources
- Updated package configuration for better compatibility

### 0.1.0
- Initial release
- Basic Markdown report generation
- Support for custom metadata via `extras` fixture
- Comprehensive test outcome tracking
- Beautiful formatting with emojis and structured sections
