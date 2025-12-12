# Development Setup

This guide helps you set up the development environment for cesiumjs_anywidget.

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alex-PLACET/cesiumjs_anywidget.git
   cd cesiumjs_anywidget
   ```

2. **Install in editable mode with development dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```

3. **Enable hot module replacement (optional but recommended):**
   ```bash
   export ANYWIDGET_HMR=1
   ```

4. **Launch JupyterLab:**
   ```bash
   jupyter lab
   ```

5. **Open the demo notebook:**
   Navigate to `examples/demo.ipynb` and run the cells.

## Project Structure

```
cesiumjs_anywidget/
├── src/cesiumjs_anywidget/
│   ├── __init__.py          # Package initialization
│   ├── widget.py            # CesiumWidget Python class
│   ├── index.js             # JavaScript render module (ESM)
│   └── styles.css           # Widget styles
├── examples/
│   └── demo.ipynb           # Demonstration notebook
├── pyproject.toml           # Package configuration
├── README.md                # User documentation
└── LICENSE                  # Apache 2.0 license
```

## Development Workflow

1. **Edit the code:**
   - Modify Python code in `src/cesiumjs_anywidget/widget.py`
   - Modify JavaScript in `src/cesiumjs_anywidget/index.js`
   - Modify CSS in `src/cesiumjs_anywidget/styles.css`

2. **Test changes:**
   - With HMR enabled, JavaScript/CSS changes reload automatically
   - For Python changes, restart the kernel and reimport

3. **Run tests:**
   ```bash
   pytest
   # or with coverage
   pytest --cov=cesiumjs_anywidget
   ```

4. **Test in notebook:**
   - Use `examples/demo.ipynb` to test functionality
   - Add new examples as needed

## Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cesiumjs_anywidget --cov-report=html

# Run specific test file
pytest tests/test_widget.py

# Run specific test
pytest tests/test_widget.py::TestWidgetInitialization::test_widget_creation

# Use make commands
make test
make test-cov
```

### Test Structure

- `tests/test_widget.py` - Widget initialization and configuration tests
- `tests/test_methods.py` - Widget method tests (fly_to, set_view, etc.)
- `tests/test_integration.py` - Integration and package tests
- `tests/conftest.py` - Shared fixtures and configuration

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Tips

- **Hot Module Replacement:** Set `ANYWIDGET_HMR=1` for automatic JS/CSS reloading
- **Browser Console:** Use developer tools to debug JavaScript issues
- **Widget State:** Use `widget.get_state()` to inspect current state
- **CesiumJS Docs:** Refer to https://cesium.com/learn/cesiumjs/ref-doc/

## Common Issues

### Import errors for anywidget or traitlets
Make sure dependencies are installed:
```bash
uv pip install anywidget traitlets
```

### Widget not displaying
- Ensure JupyterLab is version 4.0 or higher
- Try restarting the kernel
- Check browser console for errors

### CesiumJS fails to load
- Check internet connection (CesiumJS loads from CDN)
- Verify no browser extensions block CDN content
- Check browser console for CORS or network errors

## Building for Distribution

To build the package for distribution:

```bash
pip install build
python -m build
```

This creates a distributable package in the `dist/` directory.
