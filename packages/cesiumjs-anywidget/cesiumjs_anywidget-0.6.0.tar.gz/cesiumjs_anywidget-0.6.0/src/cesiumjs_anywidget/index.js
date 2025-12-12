// Generated bundle - DO NOT EDIT DIRECTLY. Edit files in src/cesiumjs_anywidget/js/ instead.


// src/cesiumjs_anywidget/js/logger.js
var debugEnabled = false;
function setDebugMode(enabled) {
  debugEnabled = enabled;
  if (enabled) {
    console.log("[CesiumWidget] Debug mode enabled");
  }
}
function log(prefix, ...args) {
  if (debugEnabled) {
    console.log(`[CesiumWidget:${prefix}]`, ...args);
  }
}
function warn(prefix, ...args) {
  console.warn(`[CesiumWidget:${prefix}]`, ...args);
}
function error(prefix, ...args) {
  console.error(`[CesiumWidget:${prefix}]`, ...args);
}

// src/cesiumjs_anywidget/js/viewer-init.js
var PREFIX = "ViewerInit";
async function loadCesiumJS() {
  log(PREFIX, "Loading CesiumJS...");
  if (window.Cesium) {
    log(PREFIX, "CesiumJS already loaded, reusing existing instance");
    return window.Cesium;
  }
  const script = document.createElement("script");
  script.src = "https://cesium.com/downloads/cesiumjs/releases/1.135/Build/Cesium/Cesium.js";
  log(PREFIX, "Loading CesiumJS from CDN...");
  await new Promise((resolve, reject) => {
    script.onload = () => {
      log(PREFIX, "CesiumJS script loaded successfully");
      resolve();
    };
    script.onerror = (err) => {
      error(PREFIX, "Failed to load CesiumJS script:", err);
      reject(err);
    };
    document.head.appendChild(script);
  });
  log(PREFIX, "CesiumJS initialized");
  return window.Cesium;
}
function createLoadingIndicator(container, hasToken) {
  const loadingDiv = document.createElement("div");
  loadingDiv.textContent = "Loading CesiumJS...";
  loadingDiv.style.cssText = "position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 18px; color: #fff; background: rgba(0,0,0,0.7); padding: 20px; border-radius: 5px;";
  if (!hasToken) {
    loadingDiv.innerHTML = `
      <div style="text-align: center;">
        <div>Loading CesiumJS...</div>
        <div style="font-size: 12px; margin-top: 10px; color: #ffa500;">
          \u26A0\uFE0F No Cesium Ion token set<br>
          Some features may not work
        </div>
      </div>
    `;
  }
  container.appendChild(loadingDiv);
  return loadingDiv;
}
function createViewer(container, model, Cesium) {
  log(PREFIX, "Creating viewer with options...");
  const viewerOptions = {
    timeline: model.get("show_timeline"),
    animation: model.get("show_animation"),
    baseLayerPicker: true,
    geocoder: true,
    homeButton: true,
    sceneModePicker: true,
    navigationHelpButton: true,
    fullscreenButton: true,
    scene3DOnly: false,
    shadows: false,
    shouldAnimate: false
  };
  log(PREFIX, "Viewer options:", viewerOptions);
  if (model.get("enable_terrain")) {
    viewerOptions.terrain = Cesium.Terrain.fromWorldTerrain();
    log(PREFIX, "Terrain enabled");
  }
  const viewer = new Cesium.Viewer(container, viewerOptions);
  viewer.scene.globe.enableLighting = model.get("enable_lighting");
  log(PREFIX, "Viewer created, lighting:", model.get("enable_lighting"));
  return viewer;
}
function setupViewerListeners(viewer, model, container, Cesium) {
  log(PREFIX, "Setting up viewer listeners");
  let isDestroyed = false;
  let scrubTimeout = null;
  model.on("change:enable_terrain", () => {
    if (isDestroyed) {
      log(PREFIX, "Skipping enable_terrain change - destroyed");
      return;
    }
    if (!viewer)
      return;
    log(PREFIX, "Terrain setting changed:", model.get("enable_terrain"));
    if (model.get("enable_terrain")) {
      viewer.scene.setTerrain(Cesium.Terrain.fromWorldTerrain());
    } else {
      viewer.scene.setTerrain(void 0);
    }
  });
  model.on("change:enable_lighting", () => {
    if (isDestroyed)
      return;
    if (!viewer)
      return;
    log(PREFIX, "Lighting setting changed:", model.get("enable_lighting"));
    viewer.scene.globe.enableLighting = model.get("enable_lighting");
  });
  model.on("change:height", () => {
    if (isDestroyed)
      return;
    if (!viewer)
      return;
    log(PREFIX, "Height changed:", model.get("height"));
    container.style.height = model.get("height");
    viewer.resize();
  });
  model.on("change:show_timeline", () => {
    if (isDestroyed)
      return;
    if (!viewer || !viewer.timeline)
      return;
    log(PREFIX, "Timeline visibility changed:", model.get("show_timeline"));
    viewer.timeline.container.style.visibility = model.get("show_timeline") ? "visible" : "hidden";
  });
  model.on("change:show_animation", () => {
    if (isDestroyed)
      return;
    if (!viewer || !viewer.animation)
      return;
    log(PREFIX, "Animation visibility changed:", model.get("show_animation"));
    viewer.animation.container.style.visibility = model.get("show_animation") ? "visible" : "hidden";
  });
  model.on("change:atmosphere_settings", () => {
    if (isDestroyed)
      return;
    if (!viewer || !viewer.scene || !viewer.scene.atmosphere)
      return;
    const settings = model.get("atmosphere_settings");
    if (!settings || Object.keys(settings).length === 0)
      return;
    log(PREFIX, "Atmosphere settings changed:", settings);
    const atmosphere = viewer.scene.atmosphere;
    if (settings.brightnessShift !== void 0) {
      atmosphere.brightnessShift = settings.brightnessShift;
    }
    if (settings.hueShift !== void 0) {
      atmosphere.hueShift = settings.hueShift;
    }
    if (settings.saturationShift !== void 0) {
      atmosphere.saturationShift = settings.saturationShift;
    }
    if (settings.lightIntensity !== void 0) {
      atmosphere.lightIntensity = settings.lightIntensity;
    }
    if (settings.rayleighCoefficient !== void 0 && Array.isArray(settings.rayleighCoefficient) && settings.rayleighCoefficient.length === 3) {
      atmosphere.rayleighCoefficient = new Cesium.Cartesian3(
        settings.rayleighCoefficient[0],
        settings.rayleighCoefficient[1],
        settings.rayleighCoefficient[2]
      );
    }
    if (settings.rayleighScaleHeight !== void 0) {
      atmosphere.rayleighScaleHeight = settings.rayleighScaleHeight;
    }
    if (settings.mieCoefficient !== void 0 && Array.isArray(settings.mieCoefficient) && settings.mieCoefficient.length === 3) {
      atmosphere.mieCoefficient = new Cesium.Cartesian3(
        settings.mieCoefficient[0],
        settings.mieCoefficient[1],
        settings.mieCoefficient[2]
      );
    }
    if (settings.mieScaleHeight !== void 0) {
      atmosphere.mieScaleHeight = settings.mieScaleHeight;
    }
    if (settings.mieAnisotropy !== void 0) {
      atmosphere.mieAnisotropy = settings.mieAnisotropy;
    }
  });
  model.on("change:sky_atmosphere_settings", () => {
    if (isDestroyed)
      return;
    if (!viewer || !viewer.scene || !viewer.scene.skyAtmosphere)
      return;
    const settings = model.get("sky_atmosphere_settings");
    if (!settings || Object.keys(settings).length === 0)
      return;
    log(PREFIX, "Sky atmosphere settings changed:", settings);
    const skyAtmosphere = viewer.scene.skyAtmosphere;
    if (settings.show !== void 0) {
      skyAtmosphere.show = settings.show;
    }
    if (settings.brightnessShift !== void 0) {
      skyAtmosphere.brightnessShift = settings.brightnessShift;
    }
    if (settings.hueShift !== void 0) {
      skyAtmosphere.hueShift = settings.hueShift;
    }
    if (settings.saturationShift !== void 0) {
      skyAtmosphere.saturationShift = settings.saturationShift;
    }
    if (settings.atmosphereLightIntensity !== void 0) {
      skyAtmosphere.atmosphereLightIntensity = settings.atmosphereLightIntensity;
    }
    if (settings.atmosphereRayleighCoefficient !== void 0 && Array.isArray(settings.atmosphereRayleighCoefficient) && settings.atmosphereRayleighCoefficient.length === 3) {
      skyAtmosphere.atmosphereRayleighCoefficient = new Cesium.Cartesian3(
        settings.atmosphereRayleighCoefficient[0],
        settings.atmosphereRayleighCoefficient[1],
        settings.atmosphereRayleighCoefficient[2]
      );
    }
    if (settings.atmosphereRayleighScaleHeight !== void 0) {
      skyAtmosphere.atmosphereRayleighScaleHeight = settings.atmosphereRayleighScaleHeight;
    }
    if (settings.atmosphereMieCoefficient !== void 0 && Array.isArray(settings.atmosphereMieCoefficient) && settings.atmosphereMieCoefficient.length === 3) {
      skyAtmosphere.atmosphereMieCoefficient = new Cesium.Cartesian3(
        settings.atmosphereMieCoefficient[0],
        settings.atmosphereMieCoefficient[1],
        settings.atmosphereMieCoefficient[2]
      );
    }
    if (settings.atmosphereMieScaleHeight !== void 0) {
      skyAtmosphere.atmosphereMieScaleHeight = settings.atmosphereMieScaleHeight;
    }
    if (settings.atmosphereMieAnisotropy !== void 0) {
      skyAtmosphere.atmosphereMieAnisotropy = settings.atmosphereMieAnisotropy;
    }
    if (settings.perFragmentAtmosphere !== void 0) {
      skyAtmosphere.perFragmentAtmosphere = settings.perFragmentAtmosphere;
    }
  });
  model.on("change:skybox_settings", () => {
    if (isDestroyed)
      return;
    if (!viewer || !viewer.scene || !viewer.scene.skyBox)
      return;
    const settings = model.get("skybox_settings");
    if (!settings || Object.keys(settings).length === 0)
      return;
    log(PREFIX, "SkyBox settings changed:", settings);
    const skyBox = viewer.scene.skyBox;
    if (settings.show !== void 0) {
      skyBox.show = settings.show;
    }
    if (settings.sources !== void 0 && settings.sources !== null) {
      const sources = settings.sources;
      if (sources.positiveX && sources.negativeX && sources.positiveY && sources.negativeY && sources.positiveZ && sources.negativeZ) {
        viewer.scene.skyBox = new Cesium.SkyBox({
          sources: {
            positiveX: sources.positiveX,
            negativeX: sources.negativeX,
            positiveY: sources.positiveY,
            negativeY: sources.negativeY,
            positiveZ: sources.positiveZ,
            negativeZ: sources.negativeZ
          }
        });
        if (settings.show !== void 0) {
          viewer.scene.skyBox.show = settings.show;
        }
      }
    }
  });
  function getCameraState() {
    if (!viewer || !viewer.camera || !viewer.camera.positionCartographic) {
      warn(PREFIX, "Cannot get camera state - viewer or camera not available");
      return null;
    }
    try {
      const cartographic = viewer.camera.positionCartographic;
      return {
        latitude: Cesium.Math.toDegrees(cartographic.latitude),
        longitude: Cesium.Math.toDegrees(cartographic.longitude),
        altitude: cartographic.height,
        heading: Cesium.Math.toDegrees(viewer.camera.heading),
        pitch: Cesium.Math.toDegrees(viewer.camera.pitch),
        roll: Cesium.Math.toDegrees(viewer.camera.roll)
      };
    } catch (error2) {
      warn(PREFIX, "Error getting camera state:", error2);
      return null;
    }
  }
  function getClockState() {
    if (!viewer || !viewer.clock)
      return null;
    try {
      return {
        current_time: Cesium.JulianDate.toIso8601(viewer.clock.currentTime),
        multiplier: viewer.clock.multiplier,
        is_animating: viewer.clock.shouldAnimate
      };
    } catch (error2) {
      warn(PREFIX, "Error getting clock state:", error2);
      return null;
    }
  }
  function sendInteractionEvent(type, additionalData = {}) {
    if (isDestroyed) {
      log(PREFIX, "Skipping interaction event - destroyed:", type);
      return;
    }
    if (!viewer) {
      warn(PREFIX, "Cannot send interaction event - viewer not available");
      return;
    }
    const cameraState = getCameraState();
    if (!cameraState) {
      warn(PREFIX, "Skipping interaction event - camera state not available");
      return;
    }
    const event = {
      type,
      timestamp: (/* @__PURE__ */ new Date()).toISOString(),
      camera: cameraState,
      clock: getClockState(),
      ...additionalData
    };
    log(PREFIX, "Interaction event:", type, event);
    model.set("interaction_event", event);
    model.save_changes();
  }
  const camera = viewer.camera;
  camera.moveEnd.addEventListener(() => {
    if (isDestroyed || !viewer)
      return;
    sendInteractionEvent("camera_move");
  });
  const scene = viewer.scene;
  const handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
  handler.setInputAction((click) => {
    if (isDestroyed || !viewer || !viewer.scene || !viewer.camera)
      return;
    const pickedData = {};
    try {
      const ray = viewer.camera.getPickRay(click.position);
      if (ray && viewer.scene.globe) {
        const cartesian = viewer.scene.globe.pick(ray, viewer.scene);
        if (cartesian) {
          const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
          pickedData.picked_position = {
            latitude: Cesium.Math.toDegrees(cartographic.latitude),
            longitude: Cesium.Math.toDegrees(cartographic.longitude),
            altitude: cartographic.height
          };
        }
      }
    } catch (error2) {
      warn(PREFIX, "Error picking position:", error2);
    }
    try {
      const pickedObject = viewer.scene.pick(click.position);
      if (Cesium.defined(pickedObject) && Cesium.defined(pickedObject.id)) {
        const entity = pickedObject.id;
        pickedData.picked_entity = {
          id: entity.id,
          name: entity.name || null
        };
        if (entity.properties) {
          const props = {};
          const propertyNames = entity.properties.propertyNames;
          if (propertyNames && propertyNames.length > 0) {
            propertyNames.forEach((name) => {
              try {
                props[name] = entity.properties[name].getValue(viewer.clock.currentTime);
              } catch (e) {
              }
            });
            if (Object.keys(props).length > 0) {
              pickedData.picked_entity.properties = props;
            }
          }
        }
      }
    } catch (error2) {
      warn(PREFIX, "Error picking entity:", error2);
    }
    sendInteractionEvent("left_click", pickedData);
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
  handler.setInputAction((click) => {
    if (isDestroyed || !viewer || !viewer.scene || !viewer.camera)
      return;
    const pickedData = {};
    try {
      const ray = viewer.camera.getPickRay(click.position);
      if (ray && viewer.scene.globe) {
        const cartesian = viewer.scene.globe.pick(ray, viewer.scene);
        if (cartesian) {
          const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
          pickedData.picked_position = {
            latitude: Cesium.Math.toDegrees(cartographic.latitude),
            longitude: Cesium.Math.toDegrees(cartographic.longitude),
            altitude: cartographic.height
          };
        }
      }
    } catch (error2) {
      warn(PREFIX, "Error picking position:", error2);
    }
    sendInteractionEvent("right_click", pickedData);
  }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);
  if (viewer.timeline) {
    let timelineScrubbing = false;
    viewer.clock.onTick.addEventListener(() => {
      if (isDestroyed)
        return;
      if (viewer.timeline) {
        if (scrubTimeout) {
          clearTimeout(scrubTimeout);
          scrubTimeout = null;
        }
        scrubTimeout = setTimeout(() => {
          if (!isDestroyed && timelineScrubbing) {
            timelineScrubbing = false;
            sendInteractionEvent("timeline_scrub");
          }
        }, 500);
        timelineScrubbing = true;
      }
    });
  }
  log(PREFIX, "Viewer listeners setup complete");
}
function setupGeoJSONLoader(viewer, model, Cesium) {
  log(PREFIX, "Setting up GeoJSON loader");
  let geojsonDataSources = [];
  let isDestroyed = false;
  async function loadGeoJSONData(flyToData = true) {
    if (isDestroyed) {
      log(PREFIX, "Skipping geojson_data load - destroyed");
      return;
    }
    if (!viewer || !viewer.dataSources) {
      warn(PREFIX, "Cannot load GeoJSON - viewer or dataSources not available");
      return;
    }
    const geojsonDataArray = model.get("geojson_data");
    log(PREFIX, "Loading GeoJSON data, count:", geojsonDataArray?.length || 0);
    geojsonDataSources.forEach((dataSource) => {
      if (viewer && viewer.dataSources) {
        viewer.dataSources.remove(dataSource);
      }
    });
    geojsonDataSources = [];
    if (geojsonDataArray && Array.isArray(geojsonDataArray)) {
      for (const geojsonData of geojsonDataArray) {
        try {
          log(PREFIX, "Loading GeoJSON dataset...");
          const dataSource = await Cesium.GeoJsonDataSource.load(geojsonData, {
            stroke: Cesium.Color.HOTPINK,
            fill: Cesium.Color.PINK.withAlpha(0.5),
            strokeWidth: 3
          });
          if (viewer && viewer.dataSources) {
            viewer.dataSources.add(dataSource);
            geojsonDataSources.push(dataSource);
            log(PREFIX, "GeoJSON dataset loaded successfully");
          }
        } catch (error2) {
          error2(PREFIX, "Error loading GeoJSON:", error2);
        }
      }
      if (flyToData && geojsonDataSources.length > 0 && viewer && viewer.flyTo) {
        log(PREFIX, "Flying to GeoJSON data");
        viewer.flyTo(geojsonDataSources[0]);
      }
    }
  }
  model.on("change:geojson_data", () => loadGeoJSONData(true));
  const initialData = model.get("geojson_data");
  if (initialData && Array.isArray(initialData) && initialData.length > 0) {
    log(PREFIX, "Loading initial GeoJSON data...");
    loadGeoJSONData(true);
  }
  return {
    destroy: () => {
      log(PREFIX, "Destroying GeoJSON loader");
      isDestroyed = true;
      geojsonDataSources.forEach((dataSource) => {
        if (viewer) {
          viewer.dataSources.remove(dataSource);
        }
      });
      geojsonDataSources = [];
    }
  };
}
function setupCZMLLoader(viewer, model, Cesium) {
  log(PREFIX, "Setting up CZML loader");
  let czmlDataSources = [];
  let isDestroyed = false;
  async function loadCZMLData(flyToData = true) {
    if (isDestroyed) {
      log(PREFIX, "Skipping czml_data load - destroyed");
      return;
    }
    if (!viewer || !viewer.dataSources) {
      warn(PREFIX, "Cannot load CZML - viewer or dataSources not available");
      return;
    }
    const czmlDataArray = model.get("czml_data");
    log(PREFIX, "Loading CZML data, count:", czmlDataArray?.length || 0);
    czmlDataSources.forEach((dataSource) => {
      if (viewer && viewer.dataSources) {
        viewer.dataSources.remove(dataSource);
      }
    });
    czmlDataSources = [];
    if (czmlDataArray && Array.isArray(czmlDataArray)) {
      for (const czmlData of czmlDataArray) {
        if (Array.isArray(czmlData) && czmlData.length > 0) {
          try {
            log(PREFIX, "Loading CZML document with", czmlData.length, "packets...");
            const dataSource = await Cesium.CzmlDataSource.load(czmlData);
            if (viewer && viewer.dataSources) {
              viewer.dataSources.add(dataSource);
              czmlDataSources.push(dataSource);
              log(PREFIX, "CZML document loaded successfully, entities:", dataSource.entities.values.length);
            }
          } catch (error2) {
            error2(PREFIX, "Error loading CZML:", error2);
          }
        } else {
          warn(PREFIX, "Skipping invalid CZML data (not an array or empty):", czmlData);
        }
      }
      if (flyToData && czmlDataSources.length > 0 && viewer && viewer.flyTo) {
        log(PREFIX, "Flying to CZML data");
        viewer.flyTo(czmlDataSources[0]);
      }
    }
  }
  model.on("change:czml_data", () => loadCZMLData(true));
  const initialData = model.get("czml_data");
  if (initialData && Array.isArray(initialData) && initialData.length > 0) {
    log(PREFIX, "Loading initial CZML data...");
    loadCZMLData(true);
  }
  return {
    destroy: () => {
      log(PREFIX, "Destroying CZML loader");
      isDestroyed = true;
      czmlDataSources.forEach((dataSource) => {
        if (viewer) {
          viewer.dataSources.remove(dataSource);
        }
      });
      czmlDataSources = [];
    }
  };
}

// src/cesiumjs_anywidget/js/camera-sync.js
var PREFIX2 = "CameraSync";
function initializeCameraSync(viewer, model) {
  const Cesium = window.Cesium;
  let cameraUpdateTimeout = null;
  let isDestroyed = false;
  let syncEnabled = model.get("camera_sync_enabled") || false;
  log(PREFIX2, "Initializing camera synchronization, sync enabled:", syncEnabled);
  model.on("change:camera_sync_enabled", () => {
    syncEnabled = model.get("camera_sync_enabled");
    log(PREFIX2, "Camera sync enabled changed:", syncEnabled);
  });
  function updateCameraFromModel() {
    if (isDestroyed) {
      log(PREFIX2, "Skipping updateCameraFromModel - module destroyed");
      return;
    }
    if (!viewer) {
      warn(PREFIX2, "updateCameraFromModel called but viewer is null");
      return;
    }
    const lat = model.get("latitude");
    const lon = model.get("longitude");
    const alt = model.get("altitude");
    const heading = Cesium.Math.toRadians(model.get("heading"));
    const pitch = Cesium.Math.toRadians(model.get("pitch"));
    const roll = Cesium.Math.toRadians(model.get("roll"));
    log(PREFIX2, "Updating camera from model:", { lat, lon, alt });
    viewer.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(lon, lat, alt),
      orientation: { heading, pitch, roll }
    });
  }
  function updateModelFromCamera() {
    if (isDestroyed) {
      log(PREFIX2, "Skipping updateModelFromCamera - module destroyed");
      return;
    }
    if (!syncEnabled) {
      log(PREFIX2, "Skipping updateModelFromCamera - sync disabled");
      return;
    }
    if (!viewer) {
      warn(PREFIX2, "updateModelFromCamera called but viewer is null");
      return;
    }
    const position = viewer.camera.positionCartographic;
    const heading = viewer.camera.heading;
    const pitch = viewer.camera.pitch;
    const roll = viewer.camera.roll;
    log(PREFIX2, "Updating model from camera:", {
      lat: Cesium.Math.toDegrees(position.latitude),
      lon: Cesium.Math.toDegrees(position.longitude),
      alt: position.height
    });
    model.set("latitude", Cesium.Math.toDegrees(position.latitude));
    model.set("longitude", Cesium.Math.toDegrees(position.longitude));
    model.set("altitude", position.height);
    model.set("heading", Cesium.Math.toDegrees(heading));
    model.set("pitch", Cesium.Math.toDegrees(pitch));
    model.set("roll", Cesium.Math.toDegrees(roll));
    model.save_changes();
  }
  function handleCameraChanged() {
    if (isDestroyed) {
      log(PREFIX2, "Skipping handleCameraChanged - module destroyed");
      return;
    }
    if (!syncEnabled) {
      return;
    }
    if (cameraUpdateTimeout) {
      clearTimeout(cameraUpdateTimeout);
    }
    cameraUpdateTimeout = setTimeout(() => {
      if (!isDestroyed && syncEnabled) {
        updateModelFromCamera();
      }
    }, 500);
  }
  updateCameraFromModel();
  viewer.camera.changed.addEventListener(handleCameraChanged);
  model.on("change:latitude", updateCameraFromModel);
  model.on("change:longitude", updateCameraFromModel);
  model.on("change:altitude", updateCameraFromModel);
  model.on("change:heading", updateCameraFromModel);
  model.on("change:pitch", updateCameraFromModel);
  model.on("change:roll", updateCameraFromModel);
  model.on("change:camera_command", () => {
    if (isDestroyed) {
      log(PREFIX2, "Skipping camera_command - module destroyed");
      return;
    }
    const command = model.get("camera_command");
    if (!command || !command.command || !command.timestamp)
      return;
    const cmd = command.command;
    log(PREFIX2, "Executing camera command:", cmd, command);
    try {
      switch (cmd) {
        case "flyTo":
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(
              command.longitude,
              command.latitude,
              command.altitude
            ),
            orientation: {
              heading: Cesium.Math.toRadians(command.heading || 0),
              pitch: Cesium.Math.toRadians(command.pitch || -15),
              roll: Cesium.Math.toRadians(command.roll || 0)
            },
            duration: command.duration || 3
          });
          break;
        case "setView":
          viewer.camera.setView({
            destination: Cesium.Cartesian3.fromDegrees(
              command.longitude,
              command.latitude,
              command.altitude
            ),
            orientation: {
              heading: Cesium.Math.toRadians(command.heading || 0),
              pitch: Cesium.Math.toRadians(command.pitch || -15),
              roll: Cesium.Math.toRadians(command.roll || 0)
            }
          });
          break;
        case "lookAt":
          const target = Cesium.Cartesian3.fromDegrees(
            command.targetLongitude,
            command.targetLatitude,
            command.targetAltitude || 0
          );
          const offset = new Cesium.HeadingPitchRange(
            Cesium.Math.toRadians(command.offsetHeading || 0),
            Cesium.Math.toRadians(command.offsetPitch || -45),
            command.offsetRange || 1e3
          );
          viewer.camera.lookAt(target, offset);
          viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY);
          break;
        case "moveForward":
          viewer.camera.moveForward(command.distance || 100);
          break;
        case "moveBackward":
          viewer.camera.moveBackward(command.distance || 100);
          break;
        case "moveUp":
          viewer.camera.moveUp(command.distance || 100);
          break;
        case "moveDown":
          viewer.camera.moveDown(command.distance || 100);
          break;
        case "moveLeft":
          viewer.camera.moveLeft(command.distance || 100);
          break;
        case "moveRight":
          viewer.camera.moveRight(command.distance || 100);
          break;
        case "rotateLeft":
          viewer.camera.rotateLeft(Cesium.Math.toRadians(command.angle || 15));
          break;
        case "rotateRight":
          viewer.camera.rotateRight(Cesium.Math.toRadians(command.angle || 15));
          break;
        case "rotateUp":
          viewer.camera.rotateUp(Cesium.Math.toRadians(command.angle || 15));
          break;
        case "rotateDown":
          viewer.camera.rotateDown(Cesium.Math.toRadians(command.angle || 15));
          break;
        case "zoomIn":
          viewer.camera.zoomIn(command.distance || 100);
          break;
        case "zoomOut":
          viewer.camera.zoomOut(command.distance || 100);
          break;
        default:
          warn(PREFIX2, `Unknown camera command: ${cmd}`);
      }
    } catch (err) {
      error(PREFIX2, `Error executing camera command ${cmd}:`, err);
    }
  });
  return {
    updateCameraFromModel,
    updateModelFromCamera,
    destroy: () => {
      log(PREFIX2, "Destroying camera sync module");
      isDestroyed = true;
      if (cameraUpdateTimeout) {
        clearTimeout(cameraUpdateTimeout);
        cameraUpdateTimeout = null;
      }
      viewer.camera.changed.removeEventListener(handleCameraChanged);
      log(PREFIX2, "Camera sync module destroyed");
    }
  };
}

// src/cesiumjs_anywidget/js/measurement-tools.js
var PREFIX3 = "Measurements";
function initializeMeasurementTools(viewer, model, container) {
  log(PREFIX3, "Initializing measurement tools");
  const Cesium = window.Cesium;
  let measurementHandler = null;
  let editHandler = null;
  let isDestroyed = false;
  let measurementState = {
    mode: null,
    points: [],
    entities: [],
    labels: [],
    polylines: [],
    polyline: null,
    tempPolyline: null
  };
  let editState = {
    enabled: false,
    selectedPoint: null,
    selectedEntity: null,
    dragging: false,
    measurementIndex: null,
    pointIndex: null
  };
  let completedMeasurements = [];
  const toolbarDiv = document.createElement("div");
  toolbarDiv.style.cssText = `
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(42, 42, 42, 0.9);
    padding: 10px;
    border-radius: 5px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 5px;
  `;
  container.appendChild(toolbarDiv);
  function createMeasurementButton(text, mode) {
    const btn = document.createElement("button");
    btn.textContent = text;
    btn.style.cssText = `
      padding: 8px 12px;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
      font-size: 12px;
      transition: background 0.2s;
    `;
    btn.onmouseover = () => {
      btn.style.background = "#2980b9";
    };
    btn.onmouseout = () => {
      btn.style.background = measurementState.mode === mode ? "#e74c3c" : "#3498db";
    };
    btn.onclick = () => {
      if (measurementState.mode === mode) {
        model.set("measurement_mode", "");
        model.save_changes();
      } else {
        model.set("measurement_mode", mode);
        model.save_changes();
      }
    };
    return btn;
  }
  const distanceBtn = createMeasurementButton("\u{1F4CF} Distance", "distance");
  const multiDistanceBtn = createMeasurementButton("\u{1F4D0} Multi Distance", "multi-distance");
  const heightBtn = createMeasurementButton("\u{1F4CA} Height", "height");
  const areaBtn = createMeasurementButton("\u2B1B Area", "area");
  const clearBtn = document.createElement("button");
  clearBtn.textContent = "\u{1F5D1}\uFE0F Clear";
  clearBtn.style.cssText = `
    padding: 8px 12px;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    transition: background 0.2s;
  `;
  clearBtn.onmouseover = () => {
    clearBtn.style.background = "#c0392b";
  };
  clearBtn.onmouseout = () => {
    clearBtn.style.background = "#e74c3c";
  };
  clearBtn.onclick = () => {
    clearAllMeasurements();
    model.set("measurement_mode", "");
    model.set("measurement_results", []);
    model.save_changes();
  };
  toolbarDiv.appendChild(distanceBtn);
  toolbarDiv.appendChild(multiDistanceBtn);
  toolbarDiv.appendChild(heightBtn);
  toolbarDiv.appendChild(areaBtn);
  toolbarDiv.appendChild(clearBtn);
  const editBtn = document.createElement("button");
  editBtn.textContent = "\u270F\uFE0F Edit Points";
  editBtn.style.cssText = `
    padding: 8px 12px;
    background: #9b59b6;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    transition: background 0.2s;
  `;
  editBtn.onmouseover = () => {
    editBtn.style.background = "#8e44ad";
  };
  editBtn.onmouseout = () => {
    editBtn.style.background = editState.enabled ? "#e74c3c" : "#9b59b6";
  };
  editBtn.onclick = () => {
    editState.enabled = !editState.enabled;
    editBtn.style.background = editState.enabled ? "#e74c3c" : "#9b59b6";
    if (editState.enabled) {
      enableEditMode();
    } else {
      disableEditMode();
    }
  };
  toolbarDiv.appendChild(editBtn);
  const editorPanel = document.createElement("div");
  editorPanel.style.cssText = `
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(42, 42, 42, 0.95);
    padding: 15px;
    border-radius: 5px;
    z-index: 1000;
    display: none;
    color: white;
    font-family: sans-serif;
    font-size: 12px;
    min-width: 250px;
  `;
  container.appendChild(editorPanel);
  const measurementsListPanel = document.createElement("div");
  measurementsListPanel.style.cssText = `
    position: absolute;
    bottom: 10px;
    right: 10px;
    background: rgba(42, 42, 42, 0.95);
    padding: 15px;
    border-radius: 5px;
    z-index: 1000;
    color: white;
    font-family: sans-serif;
    font-size: 12px;
    max-width: 350px;
    max-height: 400px;
    overflow-y: auto;
  `;
  measurementsListPanel.innerHTML = `
    <div style="font-weight: bold; border-bottom: 1px solid #555; padding-bottom: 8px; margin-bottom: 10px;">
      Measurements
    </div>
    <div id="measurements-list-content"></div>
  `;
  container.appendChild(measurementsListPanel);
  function getPosition(screenPosition) {
    const pickedObject = viewer.scene.pick(screenPosition);
    if (viewer.scene.pickPositionSupported && Cesium.defined(pickedObject)) {
      const cartesian = viewer.scene.pickPosition(screenPosition);
      if (Cesium.defined(cartesian)) {
        return cartesian;
      }
    }
    const ray = viewer.camera.getPickRay(screenPosition);
    return viewer.scene.globe.pick(ray, viewer.scene);
  }
  function addMarker(position, color = Cesium.Color.RED) {
    const marker = viewer.entities.add({
      position,
      point: {
        pixelSize: 10,
        color,
        outlineColor: Cesium.Color.WHITE,
        outlineWidth: 2,
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      }
    });
    measurementState.entities.push(marker);
    return marker;
  }
  function addLabel(position, text) {
    const label = viewer.entities.add({
      position,
      label: {
        text,
        font: "14px sans-serif",
        fillColor: Cesium.Color.WHITE,
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        outlineWidth: 2,
        outlineColor: Cesium.Color.BLACK,
        pixelOffset: new Cesium.Cartesian2(0, -20),
        showBackground: true,
        backgroundColor: Cesium.Color.fromAlpha(Cesium.Color.BLACK, 0.7),
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      }
    });
    measurementState.labels.push(label);
    return label;
  }
  function calculateDistance(point1, point2) {
    return Cesium.Cartesian3.distance(point1, point2);
  }
  function getMidpoint(point1, point2) {
    return Cesium.Cartesian3.lerp(point1, point2, 0.5, new Cesium.Cartesian3());
  }
  function cartesianToLatLonAlt(cartesian) {
    const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
    return {
      lat: Cesium.Math.toDegrees(cartographic.latitude),
      lon: Cesium.Math.toDegrees(cartographic.longitude),
      alt: cartographic.height
    };
  }
  function clearAllMeasurements() {
    log(PREFIX3, "Clearing all measurements");
    measurementState.entities.forEach((e) => viewer.entities.remove(e));
    measurementState.labels.forEach((l) => viewer.entities.remove(l));
    measurementState.polylines.forEach((p) => viewer.entities.remove(p));
    if (measurementState.polyline) {
      viewer.entities.remove(measurementState.polyline);
    }
    if (measurementState.tempPolyline) {
      viewer.entities.remove(measurementState.tempPolyline);
    }
    measurementState.points = [];
    measurementState.entities = [];
    measurementState.labels = [];
    measurementState.polylines = [];
    measurementState.polyline = null;
    measurementState.tempPolyline = null;
  }
  function clearInProgressMeasurement() {
    if (measurementState.tempPolyline) {
      viewer.entities.remove(measurementState.tempPolyline);
      measurementState.tempPolyline = null;
    }
    if ((measurementState.mode === "multi-distance" || measurementState.mode === "area") && measurementState.polyline) {
      viewer.entities.remove(measurementState.polyline);
      measurementState.polyline = null;
      measurementState.polylines = measurementState.polylines.filter((p) => p !== measurementState.polyline);
    }
    measurementState.points = [];
    measurementState.tempPoint = null;
  }
  function enableEditMode() {
    if (measurementState.mode) {
      model.set("measurement_mode", "");
      model.save_changes();
    }
    measurementState.entities.forEach((entity) => {
      if (entity.point) {
        entity.point.pixelSize = 12;
        entity.point.outlineWidth = 3;
      }
    });
    editHandler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    editHandler.setInputAction((click) => {
      const pickedObject = viewer.scene.pick(click.position);
      if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.point) {
        selectPoint(pickedObject.id, click.position);
      } else {
        deselectPoint();
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    editHandler.setInputAction((movement) => {
      if (editState.dragging && editState.selectedEntity) {
        const position = getPosition(movement.endPosition);
        if (position) {
          updatePointPosition(position);
        }
      }
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
    editHandler.setInputAction(() => {
      if (editState.selectedEntity) {
        editState.dragging = true;
        viewer.scene.screenSpaceCameraController.enableRotate = false;
      }
    }, Cesium.ScreenSpaceEventType.LEFT_DOWN);
    editHandler.setInputAction(() => {
      if (editState.dragging) {
        editState.dragging = false;
        viewer.scene.screenSpaceCameraController.enableRotate = true;
        finalizeMeasurementUpdate();
      }
    }, Cesium.ScreenSpaceEventType.LEFT_UP);
  }
  function disableEditMode() {
    if (editHandler) {
      editHandler.destroy();
      editHandler = null;
    }
    deselectPoint();
    measurementState.entities.forEach((entity) => {
      if (entity.point) {
        entity.point.pixelSize = 10;
        entity.point.outlineWidth = 2;
      }
    });
    viewer.scene.screenSpaceCameraController.enableRotate = true;
  }
  function selectPoint(entity, screenPosition) {
    const results = model.get("measurement_results") || [];
    let measurementIndex = -1;
    let pointIndex = -1;
    for (let i = 0; i < measurementState.entities.length; i++) {
      if (measurementState.entities[i] === entity) {
        let entityCount = 0;
        for (let m = 0; m < results.length; m++) {
          const measurement = results[m];
          const numPoints = measurement.points.length;
          if (i < entityCount + numPoints) {
            measurementIndex = m;
            pointIndex = i - entityCount;
            break;
          }
          entityCount += numPoints;
        }
        break;
      }
    }
    if (measurementIndex === -1)
      return;
    editState.selectedEntity = entity;
    editState.measurementIndex = measurementIndex;
    editState.pointIndex = pointIndex;
    editState.selectedPoint = entity.position.getValue(Cesium.JulianDate.now());
    entity.point.pixelSize = 15;
    entity.point.outlineWidth = 4;
    entity.point.outlineColor = Cesium.Color.YELLOW;
    showCoordinateEditor(results[measurementIndex], pointIndex);
  }
  function deselectPoint() {
    if (editState.selectedEntity && editState.selectedEntity.point) {
      editState.selectedEntity.point.pixelSize = 12;
      editState.selectedEntity.point.outlineWidth = 3;
      editState.selectedEntity.point.outlineColor = Cesium.Color.WHITE;
    }
    editState.selectedEntity = null;
    editState.selectedPoint = null;
    editState.measurementIndex = null;
    editState.pointIndex = null;
    editState.dragging = false;
    editorPanel.style.display = "none";
  }
  function showCoordinateEditor(measurement, pointIndex) {
    const point = measurement.points[pointIndex];
    editorPanel.innerHTML = `
      <div style="margin-bottom: 10px; font-weight: bold; border-bottom: 1px solid #555; padding-bottom: 5px;">
        Edit Point ${pointIndex + 1} (${measurement.type})
      </div>
      <div style="margin-bottom: 8px;">
        <label style="display: block; margin-bottom: 3px;">Longitude (\xB0):</label>
        <input type="number" id="edit-lon" value="${point.lon.toFixed(6)}" step="0.000001" 
               style="width: 100%; padding: 5px; border-radius: 3px; border: 1px solid #555; background: #2c2c2c; color: white;">
      </div>
      <div style="margin-bottom: 8px;">
        <label style="display: block; margin-bottom: 3px;">Latitude (\xB0):</label>
        <input type="number" id="edit-lat" value="${point.lat.toFixed(6)}" step="0.000001"
               style="width: 100%; padding: 5px; border-radius: 3px; border: 1px solid #555; background: #2c2c2c; color: white;">
      </div>
      <div style="margin-bottom: 10px;">
        <label style="display: block; margin-bottom: 3px;">Altitude (m):</label>
        <input type="number" id="edit-alt" value="${point.alt.toFixed(2)}" step="1"
               style="width: 100%; padding: 5px; border-radius: 3px; border: 1px solid #555; background: #2c2c2c; color: white;">
      </div>
      <button id="apply-coords" style="width: 100%; padding: 8px; background: #27ae60; color: white; border: none; border-radius: 3px; cursor: pointer; margin-bottom: 5px;">
        Apply
      </button>
      <button id="close-editor" style="width: 100%; padding: 8px; background: #95a5a6; color: white; border: none; border-radius: 3px; cursor: pointer;">
        Close
      </button>
    `;
    editorPanel.style.display = "block";
    const applyBtn = document.getElementById("apply-coords");
    const closeBtn = document.getElementById("close-editor");
    const editLonInput = document.getElementById("edit-lon");
    const editLatInput = document.getElementById("edit-lat");
    const editAltInput = document.getElementById("edit-alt");
    if (!applyBtn || !closeBtn || !editLonInput || !editLatInput || !editAltInput) {
      warn(PREFIX3, "Editor panel input elements not found in DOM");
    }
    if (applyBtn) {
      applyBtn.onclick = () => {
        if (!editLonInput || !editLatInput || !editAltInput) {
          warn(PREFIX3, "Editor input fields not available");
          return;
        }
        const lon = parseFloat(editLonInput.value);
        const lat = parseFloat(editLatInput.value);
        const alt = parseFloat(editAltInput.value);
        const newPosition = Cesium.Cartesian3.fromDegrees(lon, lat, alt);
        updatePointPosition(newPosition);
        finalizeMeasurementUpdate();
      };
    }
    if (closeBtn) {
      closeBtn.onclick = () => {
        deselectPoint();
      };
    }
    ["edit-lon", "edit-lat", "edit-alt"].forEach((id) => {
      const element = document.getElementById(id);
      if (element) {
        element.onkeypress = (e) => {
          if (e.key === "Enter" && applyBtn) {
            applyBtn.click();
          }
        };
      }
    });
  }
  function updatePointPosition(newPosition) {
    if (!editState.selectedEntity)
      return;
    editState.selectedEntity.position = newPosition;
    editState.selectedPoint = newPosition;
    updateMeasurementVisuals();
  }
  function updateMeasurementVisuals() {
    const results = model.get("measurement_results") || [];
    if (editState.measurementIndex === null)
      return;
    const measurement = results[editState.measurementIndex];
    let entityStartIndex = 0;
    for (let i = 0; i < editState.measurementIndex; i++) {
      entityStartIndex += results[i].points.length;
    }
    const positions = [];
    for (let i = 0; i < measurement.points.length; i++) {
      const entity = measurementState.entities[entityStartIndex + i];
      if (entity && entity.position) {
        positions.push(entity.position.getValue(Cesium.JulianDate.now()));
      }
    }
    const polylineStartIndex = editState.measurementIndex;
    if (measurementState.polylines[polylineStartIndex]) {
      const oldEntity = measurementState.polylines[polylineStartIndex];
      if (measurement.type === "area" && oldEntity.polygon) {
        viewer.entities.remove(oldEntity);
        const newPolygon = viewer.entities.add({
          polygon: {
            hierarchy: new Cesium.PolygonHierarchy(positions),
            material: Cesium.Color.ORANGE.withAlpha(0.3),
            outline: true,
            outlineColor: Cesium.Color.ORANGE,
            outlineWidth: 2
          }
        });
        measurementState.polylines[polylineStartIndex] = newPolygon;
      } else if (oldEntity.polyline) {
        if (measurement.type === "height") {
          const carto0 = Cesium.Cartographic.fromCartesian(positions[0]);
          const carto1 = Cesium.Cartographic.fromCartesian(positions[1]);
          oldEntity.polyline.positions = [
            positions[0],
            Cesium.Cartesian3.fromRadians(carto1.longitude, carto1.latitude, carto0.height),
            positions[1]
          ];
        } else {
          oldEntity.polyline.positions = positions;
        }
      }
    }
    updateMeasurementLabels(measurement.type, positions);
  }
  function updateMeasurementLabels(type, positions) {
    const labelStartIndex = editState.measurementIndex;
    if (type === "distance") {
      const distance = Cesium.Cartesian3.distance(positions[0], positions[1]);
      const midpoint = Cesium.Cartesian3.midpoint(positions[0], positions[1], new Cesium.Cartesian3());
      const distanceText = distance >= 1e3 ? `${(distance / 1e3).toFixed(2)} km` : `${distance.toFixed(2)} m`;
      if (measurementState.labels[labelStartIndex]) {
        measurementState.labels[labelStartIndex].position = midpoint;
        measurementState.labels[labelStartIndex].label.text = distanceText;
      }
    } else if (type === "height") {
      const carto0 = Cesium.Cartographic.fromCartesian(positions[0]);
      const carto1 = Cesium.Cartographic.fromCartesian(positions[1]);
      const verticalDistance = Math.abs(carto1.height - carto0.height);
      const midHeight = (carto0.height + carto1.height) / 2;
      const labelPos = Cesium.Cartesian3.fromRadians(carto1.longitude, carto1.latitude, midHeight);
      const heightText = verticalDistance >= 1e3 ? `${(verticalDistance / 1e3).toFixed(2)} km` : `${verticalDistance.toFixed(2)} m`;
      if (measurementState.labels[labelStartIndex]) {
        measurementState.labels[labelStartIndex].position = labelPos;
        measurementState.labels[labelStartIndex].label.text = heightText;
      }
    }
  }
  function finalizeMeasurementUpdate() {
    if (editState.measurementIndex === null || editState.pointIndex === null)
      return;
    const results = model.get("measurement_results") || [];
    const measurement = results[editState.measurementIndex];
    const cartographic = Cesium.Cartographic.fromCartesian(editState.selectedPoint);
    measurement.points[editState.pointIndex] = {
      lat: Cesium.Math.toDegrees(cartographic.latitude),
      lon: Cesium.Math.toDegrees(cartographic.longitude),
      alt: cartographic.height
    };
    let entityStartIndex = 0;
    for (let i = 0; i < editState.measurementIndex; i++) {
      entityStartIndex += results[i].points.length;
    }
    const positions = [];
    for (let i = 0; i < measurement.points.length; i++) {
      const entity = measurementState.entities[entityStartIndex + i];
      if (entity && entity.position) {
        positions.push(entity.position.getValue(Cesium.JulianDate.now()));
      }
    }
    if (measurement.type === "distance") {
      measurement.value = Cesium.Cartesian3.distance(positions[0], positions[1]);
    } else if (measurement.type === "height") {
      const carto0 = Cesium.Cartographic.fromCartesian(positions[0]);
      const carto1 = Cesium.Cartographic.fromCartesian(positions[1]);
      measurement.value = Math.abs(carto1.height - carto0.height);
    } else if (measurement.type === "multi-distance") {
      let totalDistance = 0;
      for (let i = 0; i < positions.length - 1; i++) {
        totalDistance += Cesium.Cartesian3.distance(positions[i], positions[i + 1]);
      }
      measurement.value = totalDistance;
    } else if (measurement.type === "area") {
      const polygonHierarchy = new Cesium.PolygonHierarchy(positions);
      const geometry = Cesium.PolygonGeometry.createGeometry(
        new Cesium.PolygonGeometry({
          polygonHierarchy,
          perPositionHeight: false,
          arcType: Cesium.ArcType.GEODESIC
        })
      );
      let area = 0;
      if (geometry) {
        const positionsArray = geometry.attributes.position.values;
        const indices = geometry.indices;
        for (let i = 0; i < indices.length; i += 3) {
          const i0 = indices[i] * 3;
          const i1 = indices[i + 1] * 3;
          const i2 = indices[i + 2] * 3;
          const v0 = new Cesium.Cartesian3(positionsArray[i0], positionsArray[i0 + 1], positionsArray[i0 + 2]);
          const v1 = new Cesium.Cartesian3(positionsArray[i1], positionsArray[i1 + 1], positionsArray[i1 + 2]);
          const v2 = new Cesium.Cartesian3(positionsArray[i2], positionsArray[i2 + 1], positionsArray[i2 + 2]);
          const edge1 = Cesium.Cartesian3.subtract(v1, v0, new Cesium.Cartesian3());
          const edge2 = Cesium.Cartesian3.subtract(v2, v0, new Cesium.Cartesian3());
          const crossProduct = Cesium.Cartesian3.cross(edge1, edge2, new Cesium.Cartesian3());
          const triangleArea = Cesium.Cartesian3.magnitude(crossProduct) / 2;
          area += triangleArea;
        }
      }
      measurement.value = area;
    }
    const newResults = [...results];
    model.set("measurement_results", newResults);
    model.save_changes();
    updateMeasurementsList();
    if (editorPanel.style.display !== "none") {
      showCoordinateEditor(measurement, editState.pointIndex);
    }
  }
  function updateMeasurementsList() {
    const results = model.get("measurement_results") || [];
    log(PREFIX3, "Updating measurements list, count:", results.length);
    const listContent = document.getElementById("measurements-list-content");
    if (!listContent) {
      warn(PREFIX3, "Measurements list content element not found in DOM");
      return;
    }
    if (results.length === 0) {
      listContent.innerHTML = '<div style="color: #888; font-style: italic;">No measurements yet</div>';
      return;
    }
    listContent.innerHTML = "";
    results.forEach((measurement, index) => {
      const measurementDiv = document.createElement("div");
      measurementDiv.style.cssText = `
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 3px;
        cursor: pointer;
        transition: background 0.2s;
        border-left: 3px solid ${getMeasurementColor(measurement.type)};
      `;
      measurementDiv.onmouseover = () => {
        measurementDiv.style.background = "rgba(255, 255, 255, 0.15)";
      };
      measurementDiv.onmouseout = () => {
        measurementDiv.style.background = "rgba(255, 255, 255, 0.05)";
      };
      const name = measurement.name || `${getMeasurementTypeLabel(measurement.type)} ${index + 1}`;
      const nameDiv = document.createElement("div");
      nameDiv.style.cssText = `
        font-weight: bold;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      `;
      nameDiv.innerHTML = `
        <span style="flex: 1;">${name}</span>
        <button id="rename-${index}" style="padding: 2px 6px; background: #3498db; color: white; border: none; border-radius: 2px; cursor: pointer; font-size: 10px;">\u270E</button>
      `;
      measurementDiv.appendChild(nameDiv);
      const valueDiv = document.createElement("div");
      valueDiv.style.cssText = "color: #aaa; font-size: 11px; margin-bottom: 3px;";
      valueDiv.textContent = formatMeasurementValue(measurement);
      measurementDiv.appendChild(valueDiv);
      const pointsDiv = document.createElement("div");
      pointsDiv.style.cssText = "color: #888; font-size: 10px;";
      pointsDiv.textContent = `${measurement.points.length} point${measurement.points.length > 1 ? "s" : ""}`;
      measurementDiv.appendChild(pointsDiv);
      measurementDiv.onclick = (e) => {
        if (!e.target.id.startsWith("rename-")) {
          focusOnMeasurement(index);
        }
      };
      listContent.appendChild(measurementDiv);
      const renameBtn = document.getElementById(`rename-${index}`);
      if (renameBtn) {
        renameBtn.onclick = (e) => {
          e.stopPropagation();
          renameMeasurement(index, name);
        };
      } else {
        warn(PREFIX3, `Rename button not found for measurement ${index}`);
      }
    });
  }
  function getMeasurementColor(type) {
    const colors = {
      "distance": "#e74c3c",
      "multi-distance": "#3498db",
      "height": "#2ecc71",
      "area": "#e67e22"
    };
    return colors[type] || "#95a5a6";
  }
  function getMeasurementTypeLabel(type) {
    const labels = {
      "distance": "Distance",
      "multi-distance": "Multi-Distance",
      "height": "Height",
      "area": "Area"
    };
    return labels[type] || type;
  }
  function formatMeasurementValue(measurement) {
    const value = measurement.value;
    const type = measurement.type;
    if (type === "area") {
      return value >= 1e6 ? `${(value / 1e6).toFixed(2)} km\xB2` : `${value.toFixed(2)} m\xB2`;
    } else {
      return value >= 1e3 ? `${(value / 1e3).toFixed(2)} km` : `${value.toFixed(2)} m`;
    }
  }
  function renameMeasurement(index, currentName) {
    const newName = prompt("Enter new name for measurement:", currentName);
    if (newName && newName.trim()) {
      const results = model.get("measurement_results") || [];
      const newResults = [...results];
      newResults[index] = { ...newResults[index], name: newName.trim() };
      model.set("measurement_results", newResults);
      model.save_changes();
      updateMeasurementsList();
    }
  }
  function focusOnMeasurement(index) {
    const results = model.get("measurement_results") || [];
    if (index < 0 || index >= results.length)
      return;
    const measurement = results[index];
    if (!measurement.points || measurement.points.length === 0)
      return;
    const positions = measurement.points.map(
      (p) => Cesium.Cartesian3.fromDegrees(p.lon, p.lat, p.alt || 0)
    );
    const boundingSphere = Cesium.BoundingSphere.fromPoints(positions);
    viewer.camera.flyToBoundingSphere(boundingSphere, {
      duration: 1.5,
      offset: new Cesium.HeadingPitchRange(
        0,
        Cesium.Math.toRadians(-45),
        boundingSphere.radius * 3
      )
    });
  }
  function handleDistanceClick(click) {
    const position = getPosition(click.position);
    if (!position)
      return;
    if (measurementState.points.length === 0) {
      measurementState.points.push(position);
      addMarker(position);
      measurementState.tempPolyline = viewer.entities.add({
        polyline: {
          positions: new Cesium.CallbackProperty(() => {
            if (measurementState.points.length === 1 && measurementState.tempPoint) {
              return [measurementState.points[0], measurementState.tempPoint];
            }
            return measurementState.points;
          }, false),
          width: 3,
          material: Cesium.Color.YELLOW,
          depthFailMaterial: Cesium.Color.YELLOW
        }
      });
    } else if (measurementState.points.length === 1) {
      measurementState.points.push(position);
      addMarker(position);
      const distance = calculateDistance(measurementState.points[0], measurementState.points[1]);
      const midpoint = getMidpoint(measurementState.points[0], measurementState.points[1]);
      addLabel(midpoint, `${distance.toFixed(2)} m`);
      if (measurementState.tempPolyline) {
        viewer.entities.remove(measurementState.tempPolyline);
        measurementState.tempPolyline = null;
      }
      measurementState.polyline = viewer.entities.add({
        polyline: {
          positions: measurementState.points,
          width: 3,
          material: Cesium.Color.RED,
          depthFailMaterial: Cesium.Color.RED
        }
      });
      measurementState.polylines.push(measurementState.polyline);
      const results = model.get("measurement_results") || [];
      const newResults = [...results, {
        type: "distance",
        value: distance,
        points: measurementState.points.map(cartesianToLatLonAlt),
        name: `Distance ${results.filter((r) => r.type === "distance").length + 1}`
      }];
      model.set("measurement_results", newResults);
      model.save_changes();
      measurementState.points = [];
    }
  }
  function handleMultiDistanceClick(click) {
    const position = getPosition(click.position);
    if (!position)
      return;
    measurementState.points.push(position);
    addMarker(position, Cesium.Color.BLUE);
    if (measurementState.points.length === 1) {
      measurementState.polyline = viewer.entities.add({
        polyline: {
          positions: new Cesium.CallbackProperty(() => measurementState.points, false),
          width: 3,
          material: Cesium.Color.BLUE,
          depthFailMaterial: Cesium.Color.BLUE
        }
      });
      measurementState.polylines.push(measurementState.polyline);
    } else {
      const p1 = measurementState.points[measurementState.points.length - 2];
      const p2 = measurementState.points[measurementState.points.length - 1];
      const distance = calculateDistance(p1, p2);
      const midpoint = getMidpoint(p1, p2);
      addLabel(midpoint, `${distance.toFixed(2)} m`);
      let totalDistance = 0;
      for (let i = 0; i < measurementState.points.length - 1; i++) {
        totalDistance += calculateDistance(
          measurementState.points[i],
          measurementState.points[i + 1]
        );
      }
      const results = model.get("measurement_results") || [];
      const lastResult = results[results.length - 1];
      let newResults;
      if (lastResult && lastResult.type === "multi-distance" && lastResult.isActive) {
        newResults = [...results];
        newResults[newResults.length - 1] = {
          ...lastResult,
          value: totalDistance,
          points: measurementState.points.map(cartesianToLatLonAlt)
        };
      } else {
        const multiDistanceCount = results.filter((r) => r.type === "multi-distance").length + 1;
        newResults = [...results, {
          type: "multi-distance",
          value: totalDistance,
          points: measurementState.points.map(cartesianToLatLonAlt),
          isActive: true,
          name: `Multi-Distance ${multiDistanceCount}`
        }];
      }
      model.set("measurement_results", newResults);
      model.save_changes();
    }
  }
  function handleHeightClick(click) {
    const pickedPosition = getPosition(click.position);
    if (!pickedPosition)
      return;
    const cartographic = Cesium.Cartographic.fromCartesian(pickedPosition);
    const terrainHeight = viewer.scene.globe.getHeight(cartographic) || 0;
    const pickedHeight = cartographic.height;
    const height = pickedHeight - terrainHeight;
    const groundPosition = Cesium.Cartesian3.fromRadians(
      cartographic.longitude,
      cartographic.latitude,
      terrainHeight
    );
    addMarker(groundPosition, Cesium.Color.GREEN);
    addMarker(pickedPosition, Cesium.Color.GREEN);
    const heightLine = viewer.entities.add({
      polyline: {
        positions: [groundPosition, pickedPosition],
        width: 3,
        material: Cesium.Color.GREEN,
        depthFailMaterial: Cesium.Color.GREEN
      }
    });
    measurementState.polylines.push(heightLine);
    const midpoint = getMidpoint(groundPosition, pickedPosition);
    addLabel(midpoint, `${height.toFixed(2)} m`);
    const results = model.get("measurement_results") || [];
    const newResults = [...results, {
      type: "height",
      value: height,
      points: [cartesianToLatLonAlt(groundPosition), cartesianToLatLonAlt(pickedPosition)],
      name: `Height ${results.filter((r) => r.type === "height").length + 1}`
    }];
    model.set("measurement_results", newResults);
    model.save_changes();
  }
  function handleAreaClick(click) {
    const position = getPosition(click.position);
    if (!position)
      return;
    measurementState.points.push(position);
    addMarker(position, Cesium.Color.ORANGE);
    if (measurementState.points.length === 1) {
      measurementState.polyline = viewer.entities.add({
        polygon: {
          hierarchy: new Cesium.CallbackProperty(() => {
            return new Cesium.PolygonHierarchy(measurementState.points);
          }, false),
          material: Cesium.Color.ORANGE.withAlpha(0.3),
          outline: true,
          outlineColor: Cesium.Color.ORANGE,
          outlineWidth: 2
        }
      });
      measurementState.polylines.push(measurementState.polyline);
    }
    if (measurementState.points.length >= 3) {
      const positions = measurementState.points;
      const polygonHierarchy = new Cesium.PolygonHierarchy(positions);
      const geometry = Cesium.PolygonGeometry.createGeometry(
        new Cesium.PolygonGeometry({
          polygonHierarchy,
          perPositionHeight: false,
          arcType: Cesium.ArcType.GEODESIC
        })
      );
      let area = 0;
      if (geometry) {
        const positionsArray = geometry.attributes.position.values;
        const indices = geometry.indices;
        for (let i = 0; i < indices.length; i += 3) {
          const i0 = indices[i] * 3;
          const i1 = indices[i + 1] * 3;
          const i2 = indices[i + 2] * 3;
          const v0 = new Cesium.Cartesian3(positionsArray[i0], positionsArray[i0 + 1], positionsArray[i0 + 2]);
          const v1 = new Cesium.Cartesian3(positionsArray[i1], positionsArray[i1 + 1], positionsArray[i1 + 2]);
          const v2 = new Cesium.Cartesian3(positionsArray[i2], positionsArray[i2 + 1], positionsArray[i2 + 2]);
          const edge1 = Cesium.Cartesian3.subtract(v1, v0, new Cesium.Cartesian3());
          const edge2 = Cesium.Cartesian3.subtract(v2, v0, new Cesium.Cartesian3());
          const crossProduct = Cesium.Cartesian3.cross(edge1, edge2, new Cesium.Cartesian3());
          const triangleArea = Cesium.Cartesian3.magnitude(crossProduct) / 2;
          area += triangleArea;
        }
      }
      let centroidLon = 0, centroidLat = 0;
      positions.forEach((pos) => {
        const carto = Cesium.Cartographic.fromCartesian(pos);
        centroidLon += carto.longitude;
        centroidLat += carto.latitude;
      });
      centroidLon /= positions.length;
      centroidLat /= positions.length;
      const areaText = area >= 1e6 ? `${(area / 1e6).toFixed(2)} km\xB2` : `${area.toFixed(2)} m\xB2`;
      const oldLabel = measurementState.labels.find((l) => l.label && l.label.text._value.includes("m\xB2") || l.label.text._value.includes("km\xB2"));
      if (oldLabel) {
        viewer.entities.remove(oldLabel);
        measurementState.labels = measurementState.labels.filter((l) => l !== oldLabel);
      }
      const centroidCarto = new Cesium.Cartographic(centroidLon, centroidLat);
      const promise = Cesium.sampleTerrainMostDetailed(viewer.terrainProvider, [centroidCarto]);
      promise.then(() => {
        const centroid = Cesium.Cartographic.toCartesian(centroidCarto);
        addLabel(centroid, areaText);
      });
      const results = model.get("measurement_results") || [];
      const lastResult = results[results.length - 1];
      let newResults;
      if (lastResult && lastResult.type === "area" && lastResult.isActive) {
        newResults = [...results];
        newResults[newResults.length - 1] = {
          ...lastResult,
          value: area,
          points: measurementState.points.map(cartesianToLatLonAlt)
        };
      } else {
        const areaCount = results.filter((r) => r.type === "area").length + 1;
        newResults = [...results, {
          type: "area",
          value: area,
          points: measurementState.points.map(cartesianToLatLonAlt),
          isActive: true,
          name: `Area ${areaCount}`
        }];
      }
      model.set("measurement_results", newResults);
      model.save_changes();
    }
  }
  function handleMouseMove(movement) {
    if (measurementState.mode === "distance" && measurementState.points.length === 1) {
      const position = getPosition(movement.endPosition);
      if (position) {
        measurementState.tempPoint = position;
      }
    }
  }
  function enableMeasurementMode(mode) {
    log(PREFIX3, "Enabling measurement mode:", mode);
    if (measurementHandler) {
      measurementHandler.destroy();
      measurementHandler = null;
    }
    clearInProgressMeasurement();
    measurementState.mode = mode;
    distanceBtn.style.background = mode === "distance" ? "#e74c3c" : "#3498db";
    multiDistanceBtn.style.background = mode === "multi-distance" ? "#e74c3c" : "#3498db";
    heightBtn.style.background = mode === "height" ? "#e74c3c" : "#3498db";
    areaBtn.style.background = mode === "area" ? "#e74c3c" : "#3498db";
    if (!mode)
      return;
    measurementHandler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    if (mode === "distance") {
      measurementHandler.setInputAction(handleDistanceClick, Cesium.ScreenSpaceEventType.LEFT_CLICK);
      measurementHandler.setInputAction(handleMouseMove, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
    } else if (mode === "multi-distance") {
      measurementHandler.setInputAction(handleMultiDistanceClick, Cesium.ScreenSpaceEventType.LEFT_CLICK);
      measurementHandler.setInputAction(() => {
        if (measurementState.points.length > 0) {
          const results = model.get("measurement_results") || [];
          const lastResult = results[results.length - 1];
          if (lastResult && lastResult.isActive) {
            const newResults = [...results];
            const { isActive, ...finalResult } = lastResult;
            newResults[newResults.length - 1] = finalResult;
            model.set("measurement_results", newResults);
            model.save_changes();
          }
          measurementState.points = [];
        }
      }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);
    } else if (mode === "height") {
      measurementHandler.setInputAction(handleHeightClick, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    } else if (mode === "area") {
      measurementHandler.setInputAction(handleAreaClick, Cesium.ScreenSpaceEventType.LEFT_CLICK);
      measurementHandler.setInputAction(() => {
        if (measurementState.points.length >= 3) {
          const results = model.get("measurement_results") || [];
          const lastResult = results[results.length - 1];
          if (lastResult && lastResult.isActive) {
            const newResults = [...results];
            const { isActive, ...finalResult } = lastResult;
            newResults[newResults.length - 1] = finalResult;
            model.set("measurement_results", newResults);
            model.save_changes();
          }
          measurementState.points = [];
        }
      }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);
    }
  }
  function loadAndDisplayMeasurements(measurements) {
    if (!Array.isArray(measurements))
      return;
    measurements.forEach((measurement) => {
      const { type, points } = measurement;
      if (!type || !Array.isArray(points) || points.length < 2)
        return;
      const positions = points.map((point) => {
        const [lon, lat, alt] = point;
        return Cesium.Cartesian3.fromDegrees(lon, lat, alt || 0);
      });
      if (type === "distance" && positions.length === 2) {
        displayDistance(positions);
      } else if (type === "multi-distance" && positions.length >= 2) {
        displayMultiDistance(positions);
      } else if (type === "height" && positions.length === 2) {
        displayHeight(positions);
      } else if (type === "area" && positions.length >= 3) {
        displayArea(positions);
      }
    });
  }
  function displayDistance(positions) {
    positions.forEach((pos) => addMarker(pos, Cesium.Color.RED));
    const line = viewer.entities.add({
      polyline: {
        positions,
        width: 3,
        material: Cesium.Color.RED
      }
    });
    measurementState.polylines.push(line);
    const distance = Cesium.Cartesian3.distance(positions[0], positions[1]);
    const midpoint = Cesium.Cartesian3.midpoint(positions[0], positions[1], new Cesium.Cartesian3());
    const distanceText = distance >= 1e3 ? `${(distance / 1e3).toFixed(2)} km` : `${distance.toFixed(2)} m`;
    addLabel(midpoint, distanceText);
  }
  function displayMultiDistance(positions) {
    positions.forEach((pos) => addMarker(pos, Cesium.Color.BLUE));
    const line = viewer.entities.add({
      polyline: {
        positions,
        width: 3,
        material: Cesium.Color.BLUE
      }
    });
    measurementState.polylines.push(line);
    let totalDistance = 0;
    for (let i = 0; i < positions.length - 1; i++) {
      const segmentDistance = Cesium.Cartesian3.distance(positions[i], positions[i + 1]);
      totalDistance += segmentDistance;
      const midpoint = Cesium.Cartesian3.midpoint(positions[i], positions[i + 1], new Cesium.Cartesian3());
      const segmentText = segmentDistance >= 1e3 ? `${(segmentDistance / 1e3).toFixed(2)} km` : `${segmentDistance.toFixed(2)} m`;
      addLabel(midpoint, segmentText);
    }
    const lastPos = positions[positions.length - 1];
    const totalText = totalDistance >= 1e3 ? `Total: ${(totalDistance / 1e3).toFixed(2)} km` : `Total: ${totalDistance.toFixed(2)} m`;
    addLabel(lastPos, totalText);
  }
  function displayHeight(positions) {
    positions.forEach((pos) => addMarker(pos, Cesium.Color.GREEN));
    const carto0 = Cesium.Cartographic.fromCartesian(positions[0]);
    const carto1 = Cesium.Cartographic.fromCartesian(positions[1]);
    const verticalDistance = Math.abs(carto1.height - carto0.height);
    const line = viewer.entities.add({
      polyline: {
        positions: [
          positions[0],
          Cesium.Cartesian3.fromRadians(carto1.longitude, carto1.latitude, carto0.height),
          positions[1]
        ],
        width: 3,
        material: Cesium.Color.GREEN
      }
    });
    measurementState.polylines.push(line);
    const midHeight = (carto0.height + carto1.height) / 2;
    const labelPos = Cesium.Cartesian3.fromRadians(carto1.longitude, carto1.latitude, midHeight);
    const heightText = verticalDistance >= 1e3 ? `${(verticalDistance / 1e3).toFixed(2)} km` : `${verticalDistance.toFixed(2)} m`;
    addLabel(labelPos, heightText);
  }
  function displayArea(positions) {
    positions.forEach((pos) => addMarker(pos, Cesium.Color.ORANGE));
    const polygon = viewer.entities.add({
      polygon: {
        hierarchy: new Cesium.PolygonHierarchy(positions),
        material: Cesium.Color.ORANGE.withAlpha(0.3),
        outline: true,
        outlineColor: Cesium.Color.ORANGE,
        outlineWidth: 2
      }
    });
    measurementState.polylines.push(polygon);
    const polygonHierarchy = new Cesium.PolygonHierarchy(positions);
    const geometry = Cesium.PolygonGeometry.createGeometry(
      new Cesium.PolygonGeometry({
        polygonHierarchy,
        perPositionHeight: false,
        arcType: Cesium.ArcType.GEODESIC
      })
    );
    let area = 0;
    if (geometry) {
      const positionsArray = geometry.attributes.position.values;
      const indices = geometry.indices;
      for (let i = 0; i < indices.length; i += 3) {
        const i0 = indices[i] * 3;
        const i1 = indices[i + 1] * 3;
        const i2 = indices[i + 2] * 3;
        const v0 = new Cesium.Cartesian3(positionsArray[i0], positionsArray[i0 + 1], positionsArray[i0 + 2]);
        const v1 = new Cesium.Cartesian3(positionsArray[i1], positionsArray[i1 + 1], positionsArray[i1 + 2]);
        const v2 = new Cesium.Cartesian3(positionsArray[i2], positionsArray[i2 + 1], positionsArray[i2 + 2]);
        const edge1 = Cesium.Cartesian3.subtract(v1, v0, new Cesium.Cartesian3());
        const edge2 = Cesium.Cartesian3.subtract(v2, v0, new Cesium.Cartesian3());
        const crossProduct = Cesium.Cartesian3.cross(edge1, edge2, new Cesium.Cartesian3());
        const triangleArea = Cesium.Cartesian3.magnitude(crossProduct) / 2;
        area += triangleArea;
      }
    }
    let centroidLon = 0, centroidLat = 0;
    positions.forEach((pos) => {
      const carto = Cesium.Cartographic.fromCartesian(pos);
      centroidLon += carto.longitude;
      centroidLat += carto.latitude;
    });
    centroidLon /= positions.length;
    centroidLat /= positions.length;
    const areaText = area >= 1e6 ? `${(area / 1e6).toFixed(2)} km\xB2` : `${area.toFixed(2)} m\xB2`;
    const centroidCarto = new Cesium.Cartographic(centroidLon, centroidLat);
    const promise = Cesium.sampleTerrainMostDetailed(viewer.terrainProvider, [centroidCarto]);
    promise.then(() => {
      const centroid = Cesium.Cartographic.toCartesian(centroidCarto);
      addLabel(centroid, areaText);
    });
  }
  model.on("change:measurement_mode", () => {
    if (isDestroyed) {
      log(PREFIX3, "Skipping measurement_mode change - destroyed");
      return;
    }
    const mode = model.get("measurement_mode");
    log(PREFIX3, "Measurement mode changed:", mode);
    enableMeasurementMode(mode);
  });
  model.on("change:measurement_results", () => {
    if (isDestroyed) {
      log(PREFIX3, "Skipping measurement_results change - destroyed");
      return;
    }
    const results = model.get("measurement_results") || [];
    log(PREFIX3, "Measurement results changed, count:", results.length);
    if (results.length === 0) {
      clearAllMeasurements();
    }
    updateMeasurementsList();
  });
  model.on("change:load_measurements_trigger", () => {
    if (isDestroyed)
      return;
    const triggerData = model.get("load_measurements_trigger");
    log(PREFIX3, "Load measurements trigger:", triggerData);
    if (triggerData && triggerData.measurements) {
      loadAndDisplayMeasurements(triggerData.measurements);
      updateMeasurementsList();
    }
  });
  model.on("change:focus_measurement_trigger", () => {
    if (isDestroyed)
      return;
    const triggerData = model.get("focus_measurement_trigger");
    log(PREFIX3, "Focus measurement trigger:", triggerData);
    if (triggerData && typeof triggerData.index === "number") {
      focusOnMeasurement(triggerData.index);
    }
  });
  model.on("change:show_measurement_tools", () => {
    if (isDestroyed)
      return;
    const show = model.get("show_measurement_tools");
    log(PREFIX3, "Show measurement tools:", show);
    toolbarDiv.style.display = show ? "flex" : "none";
    editorPanel.style.display = show ? editorPanel.style.display : "none";
    if (!show && editState.enabled) {
      editState.enabled = false;
      disableEditMode();
    }
  });
  model.on("change:show_measurements_list", () => {
    if (isDestroyed)
      return;
    const show = model.get("show_measurements_list");
    log(PREFIX3, "Show measurements list:", show);
    measurementsListPanel.style.display = show ? "block" : "none";
  });
  toolbarDiv.style.display = model.get("show_measurement_tools") ? "flex" : "none";
  measurementsListPanel.style.display = model.get("show_measurements_list") ? "block" : "none";
  updateMeasurementsList();
  return {
    enableMeasurementMode,
    clearAllMeasurements,
    destroy: () => {
      log(PREFIX3, "Destroying measurement tools");
      isDestroyed = true;
      if (measurementHandler) {
        measurementHandler.destroy();
      }
      clearAllMeasurements();
      if (toolbarDiv.parentNode) {
        toolbarDiv.remove();
      }
      log(PREFIX3, "Measurement tools destroyed");
    }
  };
}

// src/cesiumjs_anywidget/js/index.js
window.CESIUM_BASE_URL = "https://cesium.com/downloads/cesiumjs/releases/1.135/Build/Cesium/";
async function render({ model, el }) {
  setDebugMode(model.get("debug_mode") || false);
  model.on("change:debug_mode", () => {
    setDebugMode(model.get("debug_mode"));
  });
  log("Main", "Starting render");
  log("Main", "Loading CesiumJS...");
  const Cesium = await loadCesiumJS();
  log("Main", "CesiumJS loaded successfully");
  const container = document.createElement("div");
  container.style.width = "100%";
  container.style.height = model.get("height");
  container.style.position = "relative";
  el.appendChild(container);
  log("Main", "Container created with height:", model.get("height"));
  const ionToken = model.get("ion_access_token");
  if (ionToken) {
    Cesium.Ion.defaultAccessToken = ionToken;
    log("Main", "Ion access token set");
  } else {
    warn("Main", "No Ion access token provided");
  }
  const loadingDiv = createLoadingIndicator(container, !!ionToken);
  let viewer = null;
  let cameraSync = null;
  let measurementTools = null;
  let geoJsonLoader = null;
  let czmlLoader = null;
  (async () => {
    try {
      log("Main", "Creating Cesium Viewer...");
      viewer = createViewer(container, model, Cesium);
      log("Main", "Cesium Viewer created successfully");
      if (loadingDiv.parentNode) {
        loadingDiv.remove();
      }
      log("Main", "Initializing camera synchronization...");
      cameraSync = initializeCameraSync(viewer, model);
      log("Main", "Camera synchronization initialized");
      log("Main", "Initializing measurement tools...");
      measurementTools = initializeMeasurementTools(viewer, model, container);
      log("Main", "Measurement tools initialized");
      log("Main", "Setting up viewer listeners...");
      setupViewerListeners(viewer, model, container, Cesium);
      log("Main", "Viewer listeners set up");
      log("Main", "Setting up GeoJSON loader...");
      geoJsonLoader = setupGeoJSONLoader(viewer, model, Cesium);
      log("Main", "GeoJSON loader set up");
      log("Main", "Setting up CZML loader...");
      czmlLoader = setupCZMLLoader(viewer, model, Cesium);
      log("Main", "CZML loader set up");
      log("Main", "Initialization complete");
    } catch (err) {
      error("Main", "Error initializing CesiumJS viewer:", err);
      loadingDiv.textContent = `Error: ${err.message}`;
      loadingDiv.style.background = "rgba(255,0,0,0.8)";
    }
  })();
  return () => {
    log("Main", "Starting cleanup...");
    if (cameraSync) {
      log("Main", "Destroying camera sync...");
      cameraSync.destroy();
    }
    if (measurementTools) {
      log("Main", "Destroying measurement tools...");
      measurementTools.destroy();
    }
    if (geoJsonLoader) {
      log("Main", "Destroying GeoJSON loader...");
      geoJsonLoader.destroy();
    }
    if (czmlLoader) {
      log("Main", "Destroying CZML loader...");
      czmlLoader.destroy();
    }
    if (viewer) {
      log("Main", "Destroying viewer...");
      viewer.destroy();
    }
    log("Main", "Cleanup complete");
  };
}
var js_default = { render };
export {
  js_default as default
};
