"""CesiumJS widget implementation using anywidget."""

import os
import pathlib
import anywidget
import traitlets


class CesiumWidget(anywidget.AnyWidget):
    """A Jupyter widget for CesiumJS 3D globe visualization.

    This widget provides an interactive 3D globe with support for:
    - Camera position control (latitude, longitude, altitude)
    - Terrain and imagery visualization
    - Entity management (markers, shapes, models)
    - Bidirectional state synchronization between Python and JavaScript

    Examples
    --------
    Basic usage:
    >>> from cesiumjs_anywidget import CesiumWidget
    >>> widget = CesiumWidget()
    >>> widget  # Display in Jupyter

    Fly to a location:
    >>> widget.latitude = 40.7128
    >>> widget.longitude = -74.0060
    >>> widget.altitude = 10000

    Debugging:
    >>> widget.debug_info()  # Show debug information
    """

    # Load JavaScript and CSS from files
    _esm = pathlib.Path(__file__).parent / "index.js"
    _css = pathlib.Path(__file__).parent / "styles.css"

    # Camera position properties (synced with JavaScript)
    latitude = traitlets.Float(-122.4175, help="Camera latitude in degrees").tag(
        sync=True
    )
    longitude = traitlets.Float(37.655, help="Camera longitude in degrees").tag(
        sync=True
    )
    altitude = traitlets.Float(400.0, help="Camera altitude in meters").tag(sync=True)

    # Camera orientation
    heading = traitlets.Float(0.0, help="Camera heading in degrees").tag(sync=True)
    pitch = traitlets.Float(-15.0, help="Camera pitch in degrees").tag(sync=True)
    roll = traitlets.Float(0.0, help="Camera roll in degrees").tag(sync=True)

    # Viewer configuration
    height = traitlets.Unicode("600px", help="Widget height").tag(sync=True)

    # Viewer options
    enable_terrain = traitlets.Bool(True, help="Enable terrain visualization").tag(
        sync=True
    )
    enable_lighting = traitlets.Bool(False, help="Enable scene lighting").tag(sync=True)
    show_timeline = traitlets.Bool(True, help="Show timeline widget").tag(sync=True)
    show_animation = traitlets.Bool(True, help="Show animation widget").tag(sync=True)

    # Cesium Ion access token (optional, uses default if not set)
    ion_access_token = traitlets.Unicode("", help="Cesium Ion access token").tag(
        sync=True
    )

    # GeoJSON data for visualization (list of GeoJSON objects)
    geojson_data = traitlets.List(
        trait=traitlets.Dict(),
        default_value=[],
        help="List of GeoJSON datasets to display"
    ).tag(sync=True)

    # CZML data for visualization (list of CZML documents)
    czml_data = traitlets.List(
        trait=traitlets.List(trait=traitlets.Dict()),
        default_value=[],
        help="List of CZML documents to display",
    ).tag(sync=True)

    # Interaction event data - sent when user interaction ends
    interaction_event = traitlets.Dict(
        default_value={},
        help="Interaction event data with camera position, time, and context"
    ).tag(sync=True)

    # Atmosphere configuration
    atmosphere_settings = traitlets.Dict(
        default_value={},
        help="Atmosphere rendering settings (brightnessShift, hueShift, saturationShift, etc.)"
    ).tag(sync=True)

    # Sky atmosphere configuration
    sky_atmosphere_settings = traitlets.Dict(
        default_value={},
        help="Sky atmosphere rendering settings (show, brightnessShift, hueShift, etc.)"
    ).tag(sync=True)

    # SkyBox configuration
    skybox_settings = traitlets.Dict(
        default_value={},
        help="SkyBox rendering settings (show, sources for cube map faces)"
    ).tag(sync=True)

    # Camera commands (for advanced camera operations)
    camera_command = traitlets.Dict(
        default_value={},
        help="Camera command trigger for flyTo, lookAt, move, rotate, zoom operations"
    ).tag(sync=True)

    # Measurement tools
    measurement_mode = traitlets.Unicode(
        "",
        help="Active measurement mode: 'distance', 'multi-distance', 'height', or '' for none",
    ).tag(sync=True)
    measurement_results = traitlets.List(
        trait=traitlets.Dict(), default_value=[], help="List of measurement results"
    ).tag(sync=True)
    load_measurements_trigger = traitlets.Dict(
        default_value={}, help="Trigger to load measurements with visual display"
    ).tag(sync=True)
    focus_measurement_trigger = traitlets.Dict(
        default_value={}, help="Trigger to focus on a specific measurement"
    ).tag(sync=True)
    show_measurement_tools = traitlets.Bool(
        default_value=True, help="Show or hide measurement toolbar"
    ).tag(sync=True)
    show_measurements_list = traitlets.Bool(
        default_value=True, help="Show or hide measurements list panel"
    ).tag(sync=True)

    # Debug mode for JavaScript logging
    debug_mode = traitlets.Bool(
        default_value=False, help="Enable or disable JavaScript console logging"
    ).tag(sync=True)

    # Camera synchronization callbacks
    camera_sync_enabled = traitlets.Bool(
        default_value=False,
        help="Enable or disable camera position synchronization callbacks"
    ).tag(sync=True)

    def __init__(self, **kwargs):
        """Initialize the CesiumWidget.

        Automatically checks for CESIUM_ION_TOKEN environment variable if no token is provided.
        """
        # Check for token in environment variable if not provided
        if "ion_access_token" not in kwargs or not kwargs["ion_access_token"]:
            env_token = os.environ.get("CESIUM_ION_TOKEN", "")
            if env_token:
                kwargs["ion_access_token"] = env_token
            else:
                print("⚠️  No Cesium Ion access token provided.")
                print(
                    "   Your access token can be found at: https://ion.cesium.com/tokens"
                )
                print("   You can set it via:")
                print("   - CesiumWidget(ion_access_token='your_token')")
                print("   - export CESIUM_ION_TOKEN='your_token'  # in your shell")
                print("   Note: Some features may not work without a token.")

        super().__init__(**kwargs)

    def fly_to(self, latitude: float, longitude: float, altitude: float = 400, 
               heading: float = 0.0, pitch: float = -15.0, roll: float = 0.0,
               duration: float = 3.0):
        """Fly the camera to a specific location with animation.

        Parameters
        ----------
        latitude : float
            Target latitude in degrees
        longitude : float
            Target longitude in degrees
        altitude : float, optional
            Target altitude in meters (default: 400)
        heading : float, optional
            Camera heading in degrees (default: 0.0)
        pitch : float, optional
            Camera pitch in degrees (default: -15.0)
        roll : float, optional
            Camera roll in degrees (default: 0.0)
        duration : float, optional
            Flight duration in seconds (default: 3.0)
            
        Examples
        --------
        >>> widget.fly_to(48.8566, 2.3522, altitude=5000, duration=2.0)
        >>> widget.fly_to(40.7128, -74.0060, heading=45, pitch=-30)
        """
        import time
        # Update traitlets for state sync
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading
        self.pitch = pitch
        self.roll = roll
        # Send command for animation
        self.camera_command = {
            'command': 'flyTo',
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'heading': heading,
            'pitch': pitch,
            'roll': roll,
            'duration': duration,
            'timestamp': time.time()
        }

    def set_view(
        self, latitude: float, longitude: float, altitude: float = 400, 
        heading: float = 0.0, pitch: float = -15.0, roll: float = 0.0
    ):
        """Set the camera view instantly without animation.

        Parameters
        ----------
        latitude : float
            Camera latitude in degrees
        longitude : float
            Camera longitude in degrees
        altitude : float, optional
            Camera altitude in meters (default: 400)
        heading : float, optional
            Camera heading in degrees (default: 0.0)
        pitch : float, optional
            Camera pitch in degrees (default: -15.0)
        roll : float, optional
            Camera roll in degrees (default: 0.0)
            
        Examples
        --------
        >>> widget.set_view(48.8566, 2.3522, altitude=1000)
        >>> widget.set_view(40.7128, -74.0060, heading=90, pitch=-45)
        """
        import time
        # Update traitlets for state sync
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading
        self.pitch = pitch
        self.roll = roll
        # Send command for instant view change
        self.camera_command = {
            'command': 'setView',
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'heading': heading,
            'pitch': pitch,
            'roll': roll,
            'timestamp': time.time()
        }

    def look_at(self, target_latitude: float, target_longitude: float, target_altitude: float = 0,
                offset_heading: float = 0.0, offset_pitch: float = -45.0, offset_range: float = 1000.0):
        """Point the camera at a target location from an offset position.
        
        This is useful for looking at a specific point from a certain distance and angle.

        Parameters
        ----------
        target_latitude : float
            Target point latitude in degrees
        target_longitude : float
            Target point longitude in degrees
        target_altitude : float, optional
            Target point altitude in meters (default: 0)
        offset_heading : float, optional
            Heading offset from target in degrees (default: 0.0)
        offset_pitch : float, optional
            Pitch offset from target in degrees (default: -45.0)
        offset_range : float, optional
            Distance from target in meters (default: 1000.0)
            
        Examples
        --------
        >>> # Look at Eiffel Tower from 500m away at 30° angle
        >>> widget.look_at(48.8584, 2.2945, offset_range=500, offset_pitch=-30)
        
        >>> # Orbit view around a location
        >>> widget.look_at(40.7128, -74.0060, offset_heading=45, offset_range=2000)
        """
        import time
        self.camera_command = {
            'command': 'lookAt',
            'targetLatitude': target_latitude,
            'targetLongitude': target_longitude,
            'targetAltitude': target_altitude,
            'offsetHeading': offset_heading,
            'offsetPitch': offset_pitch,
            'offsetRange': offset_range,
            'timestamp': time.time()
        }

    def move_forward(self, distance: float = 100.0):
        """Move the camera forward by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_forward(500)  # Move 500m forward
        """
        import time
        self.camera_command = {
            'command': 'moveForward',
            'distance': distance,
            'timestamp': time.time()
        }

    def move_backward(self, distance: float = 100.0):
        """Move the camera backward by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_backward(500)  # Move 500m backward
        """
        import time
        self.camera_command = {
            'command': 'moveBackward',
            'distance': distance,
            'timestamp': time.time()
        }

    def move_up(self, distance: float = 100.0):
        """Move the camera up by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_up(200)  # Move 200m up
        """
        import time
        self.camera_command = {
            'command': 'moveUp',
            'distance': distance,
            'timestamp': time.time()
        }

    def move_down(self, distance: float = 100.0):
        """Move the camera down by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_down(200)  # Move 200m down
        """
        import time
        self.camera_command = {
            'command': 'moveDown',
            'distance': distance,
            'timestamp': time.time()
        }

    def move_left(self, distance: float = 100.0):
        """Move the camera left by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_left(150)  # Move 150m left
        """
        import time
        self.camera_command = {
            'command': 'moveLeft',
            'distance': distance,
            'timestamp': time.time()
        }

    def move_right(self, distance: float = 100.0):
        """Move the camera right by a specified distance.

        Parameters
        ----------
        distance : float, optional
            Distance to move in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.move_right(150)  # Move 150m right
        """
        import time
        self.camera_command = {
            'command': 'moveRight',
            'distance': distance,
            'timestamp': time.time()
        }

    def rotate_left(self, angle: float = 15.0):
        """Rotate the camera left (counterclockwise) by a specified angle.

        Parameters
        ----------
        angle : float, optional
            Rotation angle in degrees (default: 15.0)
            
        Examples
        --------
        >>> widget.rotate_left(45)  # Rotate 45° left
        """
        import time
        self.camera_command = {
            'command': 'rotateLeft',
            'angle': angle,
            'timestamp': time.time()
        }

    def rotate_right(self, angle: float = 15.0):
        """Rotate the camera right (clockwise) by a specified angle.

        Parameters
        ----------
        angle : float, optional
            Rotation angle in degrees (default: 15.0)
            
        Examples
        --------
        >>> widget.rotate_right(45)  # Rotate 45° right
        """
        import time
        self.camera_command = {
            'command': 'rotateRight',
            'angle': angle,
            'timestamp': time.time()
        }

    def rotate_up(self, angle: float = 15.0):
        """Rotate the camera up by a specified angle.

        Parameters
        ----------
        angle : float, optional
            Rotation angle in degrees (default: 15.0)
            
        Examples
        --------
        >>> widget.rotate_up(30)  # Look up 30°
        """
        import time
        self.camera_command = {
            'command': 'rotateUp',
            'angle': angle,
            'timestamp': time.time()
        }

    def rotate_down(self, angle: float = 15.0):
        """Rotate the camera down by a specified angle.

        Parameters
        ----------
        angle : float, optional
            Rotation angle in degrees (default: 15.0)
            
        Examples
        --------
        >>> widget.rotate_down(30)  # Look down 30°
        """
        import time
        self.camera_command = {
            'command': 'rotateDown',
            'angle': angle,
            'timestamp': time.time()
        }

    def zoom_in(self, distance: float = 100.0):
        """Zoom in (move camera closer to target).

        Parameters
        ----------
        distance : float, optional
            Distance to zoom in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.zoom_in(500)  # Zoom in 500m
        """
        import time
        self.camera_command = {
            'command': 'zoomIn',
            'distance': distance,
            'timestamp': time.time()
        }

    def zoom_out(self, distance: float = 100.0):
        """Zoom out (move camera away from target).

        Parameters
        ----------
        distance : float, optional
            Distance to zoom in meters (default: 100.0)
            
        Examples
        --------
        >>> widget.zoom_out(500)  # Zoom out 500m
        """
        import time
        self.camera_command = {
            'command': 'zoomOut',
            'distance': distance,
            'timestamp': time.time()
        }

    def set_camera(
        self,
        latitude=None,
        longitude=None,
        altitude=None,
        heading=None,
        pitch=None,
        roll=None
    ):
        """Set individual camera parameters without full view reset.
        
        This allows updating only specific camera properties while keeping others unchanged.

        Parameters
        ----------
        latitude : float, optional
            Camera latitude in degrees
        longitude : float, optional
            Camera longitude in degrees
        altitude : float, optional
            Camera altitude in meters
        heading : float, optional
            Camera heading in degrees
        pitch : float, optional
            Camera pitch in degrees
        roll : float, optional
            Camera roll in degrees
            
        Examples
        --------
        >>> widget.set_camera(pitch=-45)  # Only change pitch
        >>> widget.set_camera(heading=90, altitude=5000)  # Change heading and altitude
        """
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if altitude is not None:
            self.altitude = altitude
        if heading is not None:
            self.heading = heading
        if pitch is not None:
            self.pitch = pitch
        if roll is not None:
            self.roll = roll

    def load_geojson(self, geojson, append=False):
        """Load GeoJSON data for visualization.

        Parameters
        ----------
        geojson : dict or str
            GeoJSON dictionary or GeoJSON string
        append : bool, optional
            If True, append to existing GeoJSON data. If False (default), replace existing data.
            
        Examples
        --------
        Load a single GeoJSON (replaces existing):
        >>> widget.load_geojson({"type": "FeatureCollection", "features": [...]})
        
        Load multiple GeoJSON datasets:
        >>> widget.load_geojson(geojson1)
        >>> widget.load_geojson(geojson2, append=True)  # Adds to existing data
        """
        if isinstance(geojson, str):
            import json
            geojson = json.loads(geojson)
        
        if append:
            # Append to existing list
            current_data = list(self.geojson_data)
            current_data.append(geojson)
            self.geojson_data = current_data
        else:
            # Replace existing data
            self.geojson_data = [geojson]
    
    def clear_geojson(self):
        """Clear all GeoJSON data from the viewer.
        
        Examples
        --------
        >>> widget.clear_geojson()
        """
        self.geojson_data = []

    def load_czml(self, czml: str | list, append=False):
        """Load CZML data for visualization.

        CZML (Cesium Language) is a JSON format for describing time-dynamic
        graphical scenes in Cesium. It can describe points, lines, polygons,
        models, and other graphics primitives with time-dynamic positions,
        orientations, colors, and other properties.

        Parameters
        ----------
        czml : str or list
            CZML document as a JSON string or list of packet dictionaries.
        append : bool, optional
            If True, append to existing CZML data. If False (default), replace existing data.

        Examples
        --------
        From JSON string:
        >>> czml_json = '''[
        ...     {"id": "document", "version": "1.0"},
        ...     {"id": "point", "position": {"cartographicDegrees": [-74, 40, 0]}}
        ... ]'''
        >>> widget.load_czml(czml_json)

        From list of dicts:
        >>> czml = [
        ...     {"id": "document", "version": "1.0"},
        ...     {"id": "point", "position": {"cartographicDegrees": [-74, 40, 0]}}
        ... ]
        >>> widget.load_czml(czml)
        
        Append multiple CZML documents:
        >>> widget.load_czml(czml_doc1)
        >>> widget.load_czml(czml_doc2, append=True)  # Adds to existing data
        >>> widget.load_czml(new_czml, clear_existing=True)
        """
        import json

        # Handle string input (JSON)
        if isinstance(czml, str):
            czml = json.loads(czml)

        # Ensure we have a list
        if not isinstance(czml, list):
            raise ValueError("CZML data must be a JSON string or list of packets")

        # Validate basic structure - should have at least one packet
        if len(czml) == 0:
            raise ValueError("CZML document must contain at least one packet")

        if append:
            # Append to existing list
            current_data = list(self.czml_data)
            current_data.append(czml)
            self.czml_data = current_data
        else:
            # Replace existing data
            self.czml_data = [czml]
    
    def clear_czml(self):
        """Clear all CZML data from the viewer.
        
        Examples
        --------
        >>> widget.clear_czml()
        """
        self.czml_data = []

    def enable_measurement(self, mode: str = "distance"):
        """Enable a measurement tool.

        Parameters
        ----------
        mode : str, optional
            Measurement mode to enable:
            - 'distance': Two-point distance measurement
            - 'multi-distance': Multi-point polyline measurement
            - 'height': Vertical height measurement from ground
            - 'area': Polygon area measurement
            Default: 'distance'
        """
        valid_modes = ["distance", "multi-distance", "height", "area"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Must be one of {valid_modes}")
        self.measurement_mode = mode

    def disable_measurement(self):
        """Disable the active measurement tool and clear measurements."""
        self.measurement_mode = ""
        self.measurement_results = []

    def get_measurements(self):
        """Get all measurement results.

        Returns
        -------
        list of dict
            List of measurement results, each containing:
            - type: measurement type ('distance', 'multi-distance', 'height', or 'area')
            - value: measured value in meters (or square meters for area)
            - points: list of {lat, lon, alt} coordinates
        """
        return self.measurement_results

    def clear_measurements(self):
        """Clear all measurements from the viewer."""
        self.measurement_results = []

    def load_measurements(self, measurements):
        """Load and display measurements on the map.

        Parameters
        ----------
        measurements : list of dict
            List of measurements to load and display. Each measurement should contain:
            - type: str - 'distance', 'multi-distance', 'height', or 'area'
            - points: list of [lon, lat, alt] coordinates (GeoJSON style)

        Examples
        --------
        >>> widget.load_measurements([
        ...     {
        ...         "type": "distance",
        ...         "points": [[2.3522, 48.8566, 100], [2.3550, 48.8600, 105]]
        ...     },
        ...     {
        ...         "type": "area",
        ...         "points": [[2.3522, 48.8566, 100], [2.3550, 48.8600, 105], [2.3500, 48.8620, 98]]
        ...     }
        ... ])
        """
        import time

        # Send measurements with a timestamp to trigger the change detection
        self.load_measurements_trigger = {
            "measurements": measurements,
            "timestamp": time.time(),
        }

    def focus_on_measurement(self, index : int):
        """Focus the camera on a specific measurement by index.

        Parameters
        ----------
        index : int
            The index of the measurement to focus on (0-based)

        Examples
        --------
        >>> widget.focus_on_measurement(0)  # Focus on first measurement
        >>> widget.focus_on_measurement(2)  # Focus on third measurement
        """
        import time

        self.focus_measurement_trigger = {"index": index, "timestamp": time.time()}

    def show_tools(self):
        """Show the measurement tools toolbar."""
        self.show_measurement_tools = True

    def hide_tools(self):
        """Hide the measurement tools toolbar."""
        self.show_measurement_tools = False

    def show_list(self):
        """Show the measurements list panel."""
        self.show_measurements_list = True

    def hide_list(self):
        """Hide the measurements list panel."""
        self.show_measurements_list = False

    def enable_debug(self):
        """Enable JavaScript console logging for debugging.
        
        When enabled, detailed logs will be printed to the browser console
        showing widget initialization, data loading, camera events, etc.
        
        Examples
        --------
        >>> widget.enable_debug()  # Enable logging
        >>> # ... interact with widget, check browser console for logs
        >>> widget.disable_debug()  # Disable logging when done
        """
        self.debug_mode = True

    def disable_debug(self):
        """Disable JavaScript console logging.
        
        Examples
        --------
        >>> widget.disable_debug()
        """
        self.debug_mode = False

    def enable_camera_sync(self):
        """Enable camera synchronization callbacks.
        
        When enabled, camera position changes in the Cesium viewer will be
        synchronized back to the Python model (latitude, longitude, altitude,
        heading, pitch, roll properties).
        
        Note: This is disabled by default to avoid unnecessary updates when
        you don't need to track camera position in Python.
        
        Examples
        --------
        >>> widget.enable_camera_sync()
        >>> # Move camera in the viewer...
        >>> print(widget.latitude, widget.longitude)  # Updated values
        """
        self.camera_sync_enabled = True

    def disable_camera_sync(self):
        """Disable camera synchronization callbacks.
        
        When disabled, camera movements in the viewer will not update the
        Python model properties. This is the default state.
        
        Examples
        --------
        >>> widget.disable_camera_sync()
        """
        self.camera_sync_enabled = False

    def set_atmosphere(self, 
                      brightness_shift=None, 
                      hue_shift=None, 
                      saturation_shift=None,
                      light_intensity=None,
                      rayleigh_coefficient=None,
                      rayleigh_scale_height=None,
                      mie_coefficient=None,
                      mie_scale_height=None,
                      mie_anisotropy=None):
        """Configure atmosphere rendering settings.
        
        Parameters
        ----------
        brightness_shift : float, optional
            Brightness shift to apply (-1.0 to 1.0). Default 0.0 (no shift).
            -1.0 is complete darkness, letting space show through.
        hue_shift : float, optional
            Hue shift to apply (0.0 to 1.0). Default 0.0 (no shift).
            1.0 indicates a complete rotation of hues.
        saturation_shift : float, optional
            Saturation shift to apply (-1.0 to 1.0). Default 0.0 (no shift).
            -1.0 is monochrome.
        light_intensity : float, optional
            Intensity of light for ground atmosphere color computation.
        rayleigh_coefficient : tuple of 3 floats, optional
            Rayleigh scattering coefficient (x, y, z components).
        rayleigh_scale_height : float, optional
            Rayleigh scale height in meters.
        mie_coefficient : tuple of 3 floats, optional
            Mie scattering coefficient (x, y, z components).
        mie_scale_height : float, optional
            Mie scale height in meters.
        mie_anisotropy : float, optional
            Anisotropy of medium for Mie scattering (-1.0 to 1.0).
            
        Examples
        --------
        Make atmosphere darker:
        >>> widget.set_atmosphere(brightness_shift=-0.3)
        
        Change hue (e.g., for alien planet effect):
        >>> widget.set_atmosphere(hue_shift=0.3, saturation_shift=0.2)
        
        Desaturate atmosphere:
        >>> widget.set_atmosphere(saturation_shift=-0.5)
        
        Reset to defaults:
        >>> widget.set_atmosphere(brightness_shift=0, hue_shift=0, saturation_shift=0)
        """
        settings = {}
        
        if brightness_shift is not None:
            settings['brightnessShift'] = brightness_shift
        if hue_shift is not None:
            settings['hueShift'] = hue_shift
        if saturation_shift is not None:
            settings['saturationShift'] = saturation_shift
        if light_intensity is not None:
            settings['lightIntensity'] = light_intensity
        if rayleigh_coefficient is not None:
            if len(rayleigh_coefficient) != 3:
                raise ValueError("rayleigh_coefficient must be a tuple of 3 floats")
            settings['rayleighCoefficient'] = list(rayleigh_coefficient)
        if rayleigh_scale_height is not None:
            settings['rayleighScaleHeight'] = rayleigh_scale_height
        if mie_coefficient is not None:
            if len(mie_coefficient) != 3:
                raise ValueError("mie_coefficient must be a tuple of 3 floats")
            settings['mieCoefficient'] = list(mie_coefficient)
        if mie_scale_height is not None:
            settings['mieScaleHeight'] = mie_scale_height
        if mie_anisotropy is not None:
            settings['mieAnisotropy'] = mie_anisotropy
            
        self.atmosphere_settings = settings

    def set_sky_atmosphere(self,
                          show=None,
                          brightness_shift=None,
                          hue_shift=None,
                          saturation_shift=None,
                          light_intensity=None,
                          rayleigh_coefficient=None,
                          rayleigh_scale_height=None,
                          mie_coefficient=None,
                          mie_scale_height=None,
                          mie_anisotropy=None,
                          per_fragment_atmosphere=None):
        """Configure sky atmosphere rendering settings.
        
        The sky atmosphere is drawn around the limb of the ellipsoid and is only
        visible in 3D mode (fades out in 2D/Columbus view).
        
        Parameters
        ----------
        show : bool, optional
            Whether to show the sky atmosphere.
        brightness_shift : float, optional
            Brightness shift to apply (-1.0 to 1.0). Default 0.0 (no shift).
            -1.0 is complete darkness, letting space show through.
        hue_shift : float, optional
            Hue shift to apply (0.0 to 1.0). Default 0.0 (no shift).
            1.0 indicates a complete rotation of hues.
        saturation_shift : float, optional
            Saturation shift to apply (-1.0 to 1.0). Default 0.0 (no shift).
            -1.0 is monochrome.
        light_intensity : float, optional
            Intensity of light for sky atmosphere color computation.
        rayleigh_coefficient : tuple of 3 floats, optional
            Rayleigh scattering coefficient (x, y, z components).
        rayleigh_scale_height : float, optional
            Rayleigh scale height in meters.
        mie_coefficient : tuple of 3 floats, optional
            Mie scattering coefficient (x, y, z components).
        mie_scale_height : float, optional
            Mie scale height in meters.
        mie_anisotropy : float, optional
            Anisotropy of medium for Mie scattering (-1.0 to 1.0).
        per_fragment_atmosphere : bool, optional
            Compute atmosphere per-fragment (better quality, slight performance cost).
            
        Examples
        --------
        Hide sky atmosphere:
        >>> widget.set_sky_atmosphere(show=False)
        
        Make sky darker:
        >>> widget.set_sky_atmosphere(brightness_shift=-0.3)
        
        Change sky color:
        >>> widget.set_sky_atmosphere(hue_shift=0.2, saturation_shift=0.1)
        
        Enable per-fragment rendering:
        >>> widget.set_sky_atmosphere(per_fragment_atmosphere=True)
        
        Reset:
        >>> widget.sky_atmosphere_settings = {}
        """
        settings = {}
        
        if show is not None:
            settings['show'] = show
        if brightness_shift is not None:
            settings['brightnessShift'] = brightness_shift
        if hue_shift is not None:
            settings['hueShift'] = hue_shift
        if saturation_shift is not None:
            settings['saturationShift'] = saturation_shift
        if light_intensity is not None:
            settings['atmosphereLightIntensity'] = light_intensity
        if rayleigh_coefficient is not None:
            if len(rayleigh_coefficient) != 3:
                raise ValueError("rayleigh_coefficient must be a tuple of 3 floats")
            settings['atmosphereRayleighCoefficient'] = list(rayleigh_coefficient)
        if rayleigh_scale_height is not None:
            settings['atmosphereRayleighScaleHeight'] = rayleigh_scale_height
        if mie_coefficient is not None:
            if len(mie_coefficient) != 3:
                raise ValueError("mie_coefficient must be a tuple of 3 floats")
            settings['atmosphereMieCoefficient'] = list(mie_coefficient)
        if mie_scale_height is not None:
            settings['atmosphereMieScaleHeight'] = mie_scale_height
        if mie_anisotropy is not None:
            settings['atmosphereMieAnisotropy'] = mie_anisotropy
        if per_fragment_atmosphere is not None:
            settings['perFragmentAtmosphere'] = per_fragment_atmosphere
            
        self.sky_atmosphere_settings = settings

    def set_skybox(self,
                  show=None,
                  sources=None):
        """Configure skybox rendering settings.
        
        The skybox is the cube map displayed around the scene. You can show/hide it
        or provide custom cube map sources.
        
        Parameters
        ----------
        show : bool, optional
            Whether to show the skybox.
        sources : dict, optional
            Custom cube map sources with keys:
            - 'positiveX': URL for +X face (right)
            - 'negativeX': URL for -X face (left)
            - 'positiveY': URL for +Y face (top)
            - 'negativeY': URL for -Y face (bottom)
            - 'positiveZ': URL for +Z face (front)
            - 'negativeZ': URL for -Z face (back)
            
        Examples
        --------
        Hide skybox:
        >>> widget.set_skybox(show=False)
        
        Show skybox:
        >>> widget.set_skybox(show=True)
        
        Custom skybox:
        >>> widget.set_skybox(sources={
        ...     'positiveX': 'path/to/right.jpg',
        ...     'negativeX': 'path/to/left.jpg',
        ...     'positiveY': 'path/to/top.jpg',
        ...     'negativeY': 'path/to/bottom.jpg',
        ...     'positiveZ': 'path/to/front.jpg',
        ...     'negativeZ': 'path/to/back.jpg'
        ... })
        """
        settings = {}
        
        if show is not None:
            settings['show'] = show
            
        if sources is not None:
            if not isinstance(sources, dict):
                raise ValueError("sources must be a dictionary with cube map face URLs")
            
            # Validate that all required faces are provided if sources is given
            required_faces = {'positiveX', 'negativeX', 'positiveY', 'negativeY', 'positiveZ', 'negativeZ'}
            provided_faces = set(sources.keys())
            
            if provided_faces and not required_faces.issubset(provided_faces):
                missing = required_faces - provided_faces
                raise ValueError(f"sources must include all cube map faces. Missing: {missing}")
            
            settings['sources'] = sources
            
        self.skybox_settings = settings

    def on_interaction(self, callback):
        """Register a callback for user interaction events.
        
        The callback will be called when any user interaction ends (camera movement,
        clicks, timeline scrubbing, etc.) with a dictionary containing:
        
        - type: Interaction type ('camera_move', 'left_click', 'right_click', 'timeline_scrub')
        - timestamp: ISO 8601 timestamp when interaction occurred
        - camera: Camera state (latitude, longitude, altitude, heading, pitch, roll)
        - clock: Clock state (current_time, multiplier, is_animating) if timeline enabled
        - picked_position: Coordinates of clicked location (if applicable)
        - picked_entity: Information about clicked entity (if applicable)
        
        Parameters
        ----------
        callback : callable
            Function to call with interaction event data: callback(event_data)
            
        Examples
        --------
        >>> def handle_interaction(event):
        ...     print(f"Interaction: {event['type']}")
        ...     print(f"Camera at: {event['camera']['latitude']}, {event['camera']['longitude']}")
        ...     if 'picked_position' in event:
        ...         print(f"Clicked: {event['picked_position']}")
        >>> 
        >>> widget.on_interaction(handle_interaction)
        """
        def wrapper(change):
            event_data = change['new']
            if event_data and event_data.get('timestamp'):  # Only call if valid event
                callback(event_data)
        
        self.observe(wrapper, names='interaction_event')
        return wrapper  # Return so user can unobserve if needed

    def debug_info(self):
        """Print debug information about the widget.

        This is useful for troubleshooting widget initialization issues.
        """
        print("=== CesiumWidget Debug Info ===")
        print(f"Widget class: {self.__class__.__name__}")
        print(f"Anywidget version: {anywidget.__version__}")

        # Check file paths (note: after widget instantiation, _esm and _css contain file contents)
        esm_path = pathlib.Path(__file__).parent / "index.js"
        css_path = pathlib.Path(__file__).parent / "styles.css"

        print("\nJavaScript file:")
        print(f"  Path: {esm_path}")
        print(f"  Exists: {esm_path.exists()}")
        if esm_path.exists():
            print(f"  Size: {esm_path.stat().st_size} bytes")
        elif isinstance(self._esm, str):
            print(f"  Content loaded: {len(self._esm)} chars")

        print("\nCSS file:")
        print(f"  Path: {css_path}")
        print(f"  Exists: {css_path.exists()}")
        if css_path.exists():
            print(f"  Size: {css_path.stat().st_size} bytes")
        elif isinstance(self._css, str):
            print(f"  Content loaded: {len(self._css)} chars")

        # Show current state
        print("\nCurrent state:")
        print(f"  Position: ({self.latitude:.4f}°, {self.longitude:.4f}°)")
        print(f"  Altitude: {self.altitude:.2f}m")
        print(f"  Height: {self.height}")
        print(f"  Terrain: {self.enable_terrain}")
        print(f"  Lighting: {self.enable_lighting}")

        print("\n💡 Debugging tips:")
        print("  1. Open browser DevTools (F12) and check the Console tab for errors")
        print("  2. Check Network tab to see if CesiumJS CDN loads successfully")
        print(
            "  3. Try: widget = CesiumWidget(enable_terrain=False) to avoid async terrain loading"
        )
        print("  4. Ensure you're using JupyterLab 4.0+ or Jupyter Notebook 7.0+")
        print("  5. Check if anywidget is properly installed: pip show anywidget")
