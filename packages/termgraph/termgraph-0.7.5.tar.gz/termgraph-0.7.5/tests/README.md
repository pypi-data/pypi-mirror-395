# Tests

This directory contains the test suite for termgraph, organized into logical groups for better maintainability and clarity.

## Test Organization

The test suite is split into focused files based on functionality:

### `test_check_data.py`

Tests for the `check_data()` function that validates input data and arguments.
- Data validation (empty labels, empty data)
- Label/data size matching
- Color validation
- Category validation
- Error handling and exit codes

### `test_data_utils.py`

Tests for utility functions that operate on data.
- `find_min()` - finding minimum values in datasets
- `find_max()` - finding maximum values in datasets  
- `find_max_label_length()` - calculating label dimensions

### `test_normalize.py`

Tests for data normalization functionality.
- Basic normalization with various datasets
- Edge cases (all zeros, negative values)
- Different width scaling
- Boundary conditions

### `test_rendering.py`

Tests for chart rendering and display functions.
- `horiz_rows()` - horizontal chart row generation
- `vertically()` - vertical chart rendering
- Chart formatting and layout

### `test_read_data.py`

Tests for data input and parsing functionality.
- File reading from various formats
- Label parsing (beginning, end, multi-word)
- Category detection
- Verbose output
- Data format validation

### `test_init.py`

Tests for initialization and setup functions.
- Argument parsing and initialization

### `test_charts.py`

Tests for chart class integration.
- BarChart rendering with Data and Args classes
- VerticalChart rendering
- Chart output validation

### Module Tests (`module-test*.py`)

Standalone executable tests that demonstrate real-world module API usage:

- **`module-test1.py`** - Multi-category data with BarChart and StackedChart
- **`module-test2.py`** - Simple bar chart, different scale charts, and histograms
- **`module-test3.py`** - Basic usage example matching README documentation

These are integration tests that run as standalone Python scripts and produce visual output.

## Running Tests

### All Tests

```bash
just test           # Run all pytest unit tests
just test-verbose   # Run all pytest tests with verbose output
just test-module    # Run module API integration tests
```

### Individual Test Files

```bash
# Run specific pytest test file
just test-file tests/test_check_data.py
just test-file tests/test_normalize.py

# Run individual module test
uv run python tests/module-test1.py
uv run python tests/module-test2.py
uv run python tests/module-test3.py
```

### Specific Tests

```bash
uv run python -m pytest tests/test_check_data.py::test_check_data_empty_labels_exits_with_one
uv run python -m pytest tests/test_normalize.py::test_normalize_with_negative_datapoint_returns_correct_results
```

## Adding New Tests

### Unit Tests (pytest)

When adding new unit tests, place them in the appropriate file based on functionality:

- **Data validation** → `test_check_data.py`
- **Math/calculation utilities** → `test_data_utils.py`
- **Data scaling/normalization** → `test_normalize.py`
- **Chart class integration** → `test_charts.py`
- **File parsing/input** → `test_read_data.py`
- **Setup/configuration** → `test_init.py`

If your test doesn't fit into any existing category, consider:

1. Whether it belongs in an existing file with a broader scope
2. Creating a new focused test file (e.g., `test_calendar.py` for calendar-specific functionality)

### Module Integration Tests

Module tests (`module-test*.py`) are standalone scripts that demonstrate real-world usage:

- Create a new `module-test#.py` file for end-to-end demonstrations
- These should be runnable directly: `uv run python tests/module-test#.py`
- Focus on realistic usage scenarios, not edge cases
- Include visual output to verify charts render correctly

## Test Conventions

- Use descriptive test names that explain what is being tested
- Include docstrings for complex test scenarios
- Use `pytest.raises(SystemExit)` for testing error conditions that call `sys.exit()`
- Mock external dependencies (files, stdout) when needed
- Keep test data realistic but minimal

## Dependencies

Tests use the following packages:
- `pytest` - Test runner and framework
- `tempfile` - For creating temporary test files
- `unittest.mock` - For mocking dependencies
- `io.StringIO` - For capturing stdout in tests

## File Structure

```
tests/
├── README.md              # This file
├── test_check_data.py     # Data validation tests
├── test_charts.py         # Chart class integration tests
├── test_data_utils.py     # Utility function tests
├── test_init.py           # Initialization tests
├── test_normalize.py      # Data normalization tests
├── test_read_data.py      # Data reading/parsing tests
├── module-test1.py        # Module API integration test (multi-category)
├── module-test2.py        # Module API integration test (various chart types)
├── module-test3.py        # Module API integration test (basic example)
└── coverage-report.sh     # Coverage report generator
```
