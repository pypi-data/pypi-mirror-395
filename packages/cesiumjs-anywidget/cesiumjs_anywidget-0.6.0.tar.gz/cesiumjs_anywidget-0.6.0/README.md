# CesiumJS Anywidget

A Jupyter widget for interactive 3D globe visualization using [CesiumJS](https://cesium.com/cesiumjs/) and [anywidget](https://anywidget.dev/).

## Features

- 🌍 **Interactive 3D Globe**: Full CesiumJS viewer integration
- 🎯 **Camera Control**: Fly to locations with smooth animations
- 🔄 **Bidirectional Sync**: Camera state syncs between Python and JavaScript
- 🗺️ **GeoJSON Support**: Load and visualize GeoJSON data
- 🏔️ **Terrain & Imagery**: World terrain and satellite imagery
- 📏 **Measurement Tools**: Built-in distance, multi-point, and height measurement tools
- ⚙️ **Highly Configurable**: Customize viewer options and UI elements

## Installation

Using uv (recommended):

```bash
uv pip install cesiumjs-anywidget
```

Or for development:

```bash
git clone https://github.com/Alex-PLACET/cesiumjs_anywidget.git
cd cesiumjs_anywidget
uv pip install -e ".[dev]"
```

## Quick Start

```python
from cesiumjs_anywidget import CesiumWidget

# Create and display the widget
widget = CesiumWidget(height="700px")
widget
```

## Usage Examples

### Fly to a Location

```python
# Fly to New York City
widget.fly_to(latitude=40.7128, longitude=-74.0060, altitude=50000)

# Fly to Mount Everest
widget.fly_to(latitude=27.9881, longitude=86.9250, altitude=20000)
```

### Advanced Camera Control

```python
# Set camera with custom orientation
widget.set_view(
    latitude=40.7128, 
    longitude=-74.0060, 
    altitude=5000,
    heading=45.0,    # Rotate view 45 degrees
    pitch=-45.0,     # Look at angle instead of straight down
    roll=0.0
)
```

### Read Camera State

```python
# Camera position is synchronized bidirectionally
print(f"Latitude: {widget.latitude:.4f}°")
print(f"Longitude: {widget.longitude:.4f}°")
print(f"Altitude: {widget.altitude:.2f} meters")
```

### Visualize GeoJSON Data

```python
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128]
            },
            "properties": {
                "name": "New York City"
            }
        }
    ]
}

widget.load_geojson(geojson_data)
```

### Visualize CZML Data

CZML (Cesium Language) is a JSON format for describing time-dynamic graphical scenes. It's particularly useful for animations and complex visualizations.

```python
# Simple CZML example - as Python list
czml_data = [
    {
        "id": "document",
        "name": "Simple CZML",
        "version": "1.0"
    },
    {
        "id": "point",
        "name": "Location",
        "position": {
            "cartographicDegrees": [-74.0060, 40.7128, 0]
        },
        "point": {
            "pixelSize": 10,
            "color": {
                "rgba": [255, 0, 0, 255]
            }
        }
    }
]

widget.load_czml(czml_data)
```

Or from a JSON string:

```python
import json

# CZML as JSON string
czml_json = json.dumps([
    {"id": "document", "version": "1.0"},
    {
        "id": "satellite",
        "position": {
            "cartographicDegrees": [-75, 40, 500000]
        },
        "point": {"pixelSize": 8, "color": {"rgba": [0, 255, 0, 255]}}
    }
])

widget.load_czml(czml_json)
```

You can use the [czml3](https://github.com/Stoops-ML/czml3) library to generate CZML more easily, then pass the output as a string or list.

### Configure Viewer Options

```python
# Create widget with custom configuration
widget = CesiumWidget(
    height="700px",
    enable_terrain=True,
    enable_lighting=True,
    show_timeline=True,
    show_animation=True,
    latitude=27.9881,
    longitude=86.9250,
    altitude=30000
)
```

## Development

Enable hot module replacement for live updates during development:

```bash
export ANYWIDGET_HMR=1
jupyter lab
```

### Running Tests

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=cesiumjs_anywidget --cov-report=html

# Or use make
make test
make test-cov
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Measurement Tools

The widget includes built-in measurement tools for spatial analysis:

### Distance Measurement

Measure the distance between two points:

```python
# Enable distance measurement mode
widget.enable_measurement(mode="distance")

# Click two points in the viewer to measure distance
# Results are automatically synced to Python
measurements = widget.get_measurements()
print(f"Distance: {measurements[0]['value']:.2f} meters")
```

### Multi-Point Distance Measurement

Measure distances along a polyline with multiple points:

```python
# Enable multi-point distance measurement
widget.enable_measurement(mode="multi-distance")

# Click multiple points to create a polyline
# Right-click to finish the measurement
# Total distance is calculated automatically
```

### Height Measurement

Measure vertical height from ground to a point (useful for buildings):

```python
# Enable height measurement
widget.enable_measurement(mode="height")

# Click on a point to measure its height above ground
measurements = widget.get_measurements()
print(f"Height: {measurements[0]['value']:.2f} meters")
```

### Managing Measurements

```python
# Get all measurement results
measurements = widget.get_measurements()
for m in measurements:
    print(f"Type: {m['type']}, Value: {m['value']:.2f}m")

# Clear all measurements
widget.clear_measurements()

# Disable measurement mode
widget.disable_measurement()
```

### Loading Measurements from Python

You can programmatically add measurements with specific coordinates:

```python
# Load a distance measurement between two points
measurements_data = [
    {
        "type": "distance",
        "name": "Bridge Length",
        "points": [
            {"coordinates": [-74.0445, 40.6892, 10]},  # [lon, lat, alt]
            {"coordinates": [-73.9626, 40.8075, 10]}
        ]
    }
]
widget.load_measurements(measurements_data)

# Load an area measurement (polygon)
area_data = [
    {
        "type": "area",
        "name": "Central Park",
        "points": [
            {"coordinates": [-73.9812, 40.7681, 0]},
            {"coordinates": [-73.9581, 40.7681, 0]},
            {"coordinates": [-73.9581, 40.8005, 0]},
            {"coordinates": [-73.9812, 40.8005, 0]}
        ]
    }
]
widget.load_measurements(area_data)

# Focus camera on a specific measurement
widget.focus_on_measurement(0)  # Focus on first measurement
```

### Controlling Measurement UI Visibility

You can show/hide the measurement tools and list panel:

```python
# Hide measurement tools (toolbar)
widget.hide_tools()
# Or: widget.show_measurement_tools = False

# Show tools again
widget.show_tools()
# Or: widget.show_measurement_tools = True

# Hide the measurements list panel
widget.hide_list()
# Or: widget.show_measurements_list = False

# Show list again
widget.show_list()
# Or: widget.show_measurements_list = True

# Create a clean viewer without measurement tools
widget = CesiumWidget(
    show_measurement_tools=False,
    show_measurements_list=False
)
```

Each measurement includes:
- `type`: Measurement type (`'distance'`, `'multi-distance'`, `'height'`, or `'area'`)
- `value`: Measured value in meters (distance) or square meters (area)
- `points`: List of coordinates with `lat`, `lon`, `alt` properties
- `name`: Optional name for the measurement (auto-generated if not provided)

## API Reference

### CesiumWidget

**Parameters:**
- `latitude` (float): Camera latitude in degrees (default: 0.0)
- `longitude` (float): Camera longitude in degrees (default: 0.0)
- `altitude` (float): Camera altitude in meters (default: 20000000.0)
- `heading` (float): Camera heading in degrees (default: 0.0)
- `pitch` (float): Camera pitch in degrees (default: -90.0)
- `roll` (float): Camera roll in degrees (default: 0.0)
- `height` (str): Widget height CSS value (default: "600px")
- `enable_terrain` (bool): Enable terrain visualization (default: True)
- `enable_lighting` (bool): Enable scene lighting (default: False)
- `show_timeline` (bool): Show timeline widget (default: False)
- `show_animation` (bool): Show animation widget (default: False)
- `ion_access_token` (str): Cesium Ion access token (optional)
- `geojson_data` (dict): GeoJSON data to display (optional)
- `czml_data` (list): CZML data to display (optional)
- `measurement_mode` (str): Active measurement mode (default: "")
- `measurement_results` (list): List of measurement results (default: [])
- `show_measurement_tools` (bool): Show measurement toolbar (default: True)
- `show_measurements_list` (bool): Show measurements list panel (default: True)

**Methods:**
- `fly_to(latitude, longitude, altitude=10000, duration=3.0)`: Fly camera to location
- `set_view(latitude, longitude, altitude=10000, heading=0.0, pitch=-90.0, roll=0.0)`: Set camera view instantly
- `load_geojson(geojson)`: Load GeoJSON data for visualization
- `load_czml(czml)`: Load CZML data for time-dynamic visualization
- `enable_measurement(mode="distance")`: Enable measurement tool (modes: 'distance', 'multi-distance', 'height', 'area')
- `disable_measurement()`: Disable measurement tool
- `get_measurements()`: Get all measurement results
- `clear_measurements()`: Clear all measurements from viewer
- `load_measurements(measurements)`: Load measurements from Python data
- `focus_on_measurement(index)`: Fly camera to specific measurement
- `show_tools()`: Show the measurement tools toolbar
- `hide_tools()`: Hide the measurement tools toolbar
- `show_list()`: Show the measurements list panel
- `hide_list()`: Hide the measurements list panel

## Examples

See the [examples](examples/) directory for Jupyter notebook demonstrations.

## Troubleshooting

If you encounter issues with widget initialization:

```python
from cesiumjs_anywidget import CesiumWidget
widget = CesiumWidget()
widget.debug_info()  # Show debug information
```

Common fixes:
- **Open browser DevTools (F12)** and check the Console tab for errors
- Try without terrain: `widget = CesiumWidget(enable_terrain=False)`
- Ensure you're using JupyterLab 4.0+ or Jupyter Notebook 7.0+
- Check internet connection (CesiumJS loads from CDN)

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed debugging guide.

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [anywidget](https://anywidget.dev/)
- Powered by [CesiumJS](https://cesium.com/cesiumjs/)
- Uses [Cesium Ion](https://cesium.com/ion/) for terrain and imagery