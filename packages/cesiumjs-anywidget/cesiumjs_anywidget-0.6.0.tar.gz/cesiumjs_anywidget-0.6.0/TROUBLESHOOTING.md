# Troubleshooting Guide for CesiumJS Anywidget

## Common Errors and Solutions

### Error: "[anywidget] Failed to initialize model"

This error typically occurs when the JavaScript module fails to load or execute. Here are the most common causes and solutions:

#### 1. **File Path Issues**

**Problem:** The `_esm` or `_css` file paths are incorrect or files don't exist.

**Solution:**
```python
from cesiumjs_anywidget import CesiumWidget
widget = CesiumWidget()
widget.debug_info()  # This will show if files exist
```

Check that:
- `src/cesiumjs_anywidget/index.js` exists
- `src/cesiumjs_anywidget/styles.css` exists
- The package was installed correctly: `uv pip install -e .`

#### 2. **JavaScript Syntax Errors**

**Problem:** There's a syntax error in the JavaScript code.

**Solution:**
- Open browser DevTools (F12)
- Check the Console tab for JavaScript errors
- Look for red error messages mentioning `index.js`

#### 3. **CesiumJS CDN Loading Issues**

**Problem:** The CesiumJS library fails to load from CDN.

**Solution:**
- Check internet connection
- Open browser DevTools → Network tab
- Look for failed requests to `esm.sh/cesium`
- Try disabling browser extensions that might block CDN content

#### 4. **Async Initialization Issues**

**Problem:** The async terrain loading causes initialization to fail.

**Solution:**
Try creating the widget without terrain initially:
```python
widget = CesiumWidget(enable_terrain=False)
widget
```

Then enable terrain after the widget loads:
```python
widget.enable_terrain = True
```

#### 5. **JupyterLab/Notebook Version Issues**

**Problem:** Older versions of Jupyter don't fully support anywidget.

**Solution:**
Ensure you're using:
- JupyterLab 4.0+ or Jupyter Notebook 7.0+

Check versions:
```bash
jupyter lab --version
jupyter notebook --version
```

Upgrade if needed:
```bash
uv pip install --upgrade jupyterlab
```

## Debugging Workflow

### Step 1: Check Python Side

```python
from cesiumjs_anywidget import CesiumWidget
widget = CesiumWidget()
widget.debug_info()
```

This will show:
- File paths and whether they exist
- Current widget state
- Helpful debugging tips

### Step 2: Check JavaScript Side

1. Open browser DevTools (F12 or right-click → Inspect)
2. Go to **Console** tab
3. Create the widget:
   ```python
   widget = CesiumWidget()
   widget
   ```
4. Look for error messages in the console

Common console errors and their meanings:

- **"Failed to fetch"** → Network/CDN issue
- **"Unexpected token"** → JavaScript syntax error
- **"Cannot read property of undefined"** → Missing dependency or initialization issue
- **"Cesium is not defined"** → CesiumJS library didn't load

### Step 3: Check Network Activity

In DevTools → **Network** tab:
1. Refresh the widget or create a new one
2. Look for requests to `esm.sh/cesium`
3. Check if they complete successfully (status 200)

### Step 4: Test with Minimal Configuration

Try the simplest possible configuration:

```python
widget = CesiumWidget(
    enable_terrain=False,
    enable_lighting=False,
    show_timeline=False,
    show_animation=False
)
widget
```

If this works, add features one by one to identify the problematic setting.

## Advanced Debugging

### Use Inline JavaScript for Testing

If file loading is problematic, test with inline JavaScript:

```python
import anywidget
import traitlets

class TestWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        el.innerHTML = "<h1>Test Widget Works!</h1>";
        console.log("Widget rendered successfully");
    }
    export default { render };
    """
    
test = TestWidget()
test
```

If this works but CesiumWidget doesn't, the issue is in the CesiumJS initialization.

### Check Package Installation

```bash
# Verify anywidget is installed
uv pip show anywidget

# Reinstall the package
cd /path/to/cesiumjs_anywidget
uv pip install -e . --force-reinstall

# Clear Jupyter cache
jupyter lab clean
```

### Enable Verbose Logging

In the browser console, you can enable verbose logging:

```javascript
// Type this in the browser DevTools console
localStorage.debug = '*';
```

Then refresh the page to see detailed logs.

## Environment-Specific Issues

### Running in Google Colab

Colab may have restrictions on loading external resources. Try:

```python
# Install in Colab
!pip install git+https://github.com/Alex-PLACET/cesiumjs_anywidget.git
```

### Running in VSCode

Make sure you have the Jupyter extension installed and enabled.

### Running Behind a Proxy/Firewall

If you're behind a corporate firewall:
- The CDN (`esm.sh`) might be blocked
- Contact your IT department to whitelist `esm.sh` and `cesium.com`

## Still Having Issues?

1. **Check the browser console** - This is the #1 debugging tool
2. **Try without terrain** - Set `enable_terrain=False`
3. **Test with minimal widget** - Use the TestWidget example above
4. **Check versions** - Ensure JupyterLab 4.0+, anywidget latest version
5. **Clear caches** - Run `jupyter lab clean` and restart

## Reporting Bugs

If you've tried all the above and still have issues, please report with:

1. Output from `widget.debug_info()`
2. Browser console errors (screenshot or copy/paste)
3. Python version: `python --version`
4. JupyterLab version: `jupyter lab --version`
5. Operating system

## Quick Reference: Essential Debugging Commands

```python
# Show debug information
widget.debug_info()

# Check if widget object exists
print(widget)

# Check widget state
print(widget.get_state())

# Test minimal widget
test = CesiumWidget(enable_terrain=False)
test
```

## Browser Console Commands

```javascript
// Check if Cesium loaded
console.log(typeof Cesium);  // Should be 'object'

// Check anywidget
console.log(window.anywidget);

// Enable verbose logging
localStorage.debug = '*';
```
