/**
 * ORCA - Ocean Risk & Condition Analyzer
 * Leaflet GIS Interactive Ocean Map Controller
 * Enhanced with PFZ, Chlorophyll, SST, Cyclone, Maritime Boundary (EEZ), and Fishing Heatmap layers
 */

let mainMap = null;
let buoyLayerGroup = null;
let pfzLayerGroup = null;
let chlorophyllLayerGroup = null;
let sstLayerGroup = null;
let cycloneLayerGroup = null;
let maritimeBoundaryLayerGroup = null;

function initOceanMap(stations, conditions, pfzZones, alerts, geojsonLayers) {
  const mapContainer = document.getElementById('ocean-map-container');
  if (!mapContainer) return;

  // Center on Indian Ocean maritime waters
  mainMap = L.map('ocean-map-container', {
    center: [14.0, 78.5],
    zoom: 5,
    zoomControl: true,
    minZoom: 4,
    maxZoom: 12
  });

  // Dark Ocean Tile Layer (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://carto.com/">CartoDB</a> | ORCA Maritime Surveillance',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(mainMap);

  // Initialize Layer Groups
  buoyLayerGroup = L.layerGroup().addTo(mainMap);
  pfzLayerGroup = L.layerGroup().addTo(mainMap);
  chlorophyllLayerGroup = L.layerGroup().addTo(mainMap);
  sstLayerGroup = L.layerGroup().addTo(mainMap);
  cycloneLayerGroup = L.layerGroup().addTo(mainMap);
  maritimeBoundaryLayerGroup = L.layerGroup().addTo(mainMap);

  // 1. Plot Maritime Boundary GeoJSON (EEZ 200 NM & Territorial 12 NM)
  if (geojsonLayers && geojsonLayers.maritime_boundaries) {
    L.geoJSON(geojsonLayers.maritime_boundaries, {
      style: (feature) => ({
        color: feature.properties.color || '#00f2fe',
        weight: feature.properties.type === 'EEZ' ? 2.5 : 1.8,
        dashArray: feature.properties.dash || '6, 6',
        opacity: 0.85
      }),
      onEachFeature: (feature, layer) => {
        layer.bindTooltip(`<strong>${feature.properties.name}</strong><br/>Type: ${feature.properties.type}`, {
          sticky: true,
          className: 'bg-dark text-white border-info'
        });
      }
    }).addTo(maritimeBoundaryLayerGroup);
  }

  // 2. Plot Chlorophyll Bloom Polygons
  if (geojsonLayers && geojsonLayers.chlorophyll_blooms) {
    L.geoJSON(geojsonLayers.chlorophyll_blooms, {
      style: (feature) => ({
        color: '#00d2d3',
        fillColor: '#00d2d3',
        fillOpacity: 0.28,
        weight: 1.5,
        dashArray: '3, 4'
      }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(`
          <div style="font-family:'Segoe UI',sans-serif;">
            <div class="badge bg-info text-dark mb-1">Chlorophyll-a Plankton Bloom</div>
            <h6 class="fw-bold text-white mb-1">${feature.properties.name}</h6>
            <div class="small text-muted">Density: <strong class="text-info">${feature.properties.chlorophyll}</strong></div>
            <div class="small text-success">Yield Potential: <strong>${feature.properties.yield}</strong></div>
          </div>
        `);
      }
    }).addTo(chlorophyllLayerGroup);
  }

  // 3. Plot SST Thermal Fronts & Eddies
  if (geojsonLayers && geojsonLayers.sst_fronts) {
    L.geoJSON(geojsonLayers.sst_fronts, {
      style: (feature) => ({
        color: feature.properties.color || '#ff9f43',
        fillColor: feature.properties.color || '#ff9f43',
        fillOpacity: 0.22,
        weight: 1.8
      }),
      onEachFeature: (feature, layer) => {
        layer.bindPopup(`
          <div style="font-family:'Segoe UI',sans-serif;">
            <div class="badge bg-warning text-dark mb-1">SST Thermal Feature</div>
            <h6 class="fw-bold text-white mb-1">${feature.properties.name}</h6>
            <div class="small text-muted">Core Temperature: <strong class="text-warning">${feature.properties.sst}</strong></div>
            <div class="small text-info">Thermal Gradient: ${feature.properties.gradient}</div>
          </div>
        `);
      }
    }).addTo(sstLayerGroup);
  }

  // 4. Plot Active Cyclone Track & Forecast Cone
  if (geojsonLayers && geojsonLayers.cyclone_track) {
    L.geoJSON(geojsonLayers.cyclone_track, {
      style: (feature) => {
        if (feature.geometry.type === 'LineString') {
          return { color: '#ee5253', weight: 3, dashArray: '4, 4' };
        } else if (feature.geometry.type === 'Polygon') {
          return { color: '#ff6b6b', fillColor: '#ee5253', fillOpacity: 0.15, weight: 1.5 };
        }
      },
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: 9,
          fillColor: '#ee5253',
          color: '#fff',
          weight: 2,
          fillOpacity: 0.95
        });
      },
      onEachFeature: (feature, layer) => {
        if (feature.properties.name) {
          layer.bindPopup(`
            <div style="font-family:'Segoe UI',sans-serif;">
              <div class="badge bg-danger mb-1">Cyclone Warning</div>
              <h6 class="fw-bold text-white mb-1">${feature.properties.name}</h6>
              ${feature.properties.wind_speed ? `<div class="small text-muted">Winds: ${feature.properties.wind_speed}</div>` : ''}
              ${feature.properties.pressure ? `<div class="small text-muted">Pressure: ${feature.properties.pressure}</div>` : ''}
              ${feature.properties.intensity ? `<div class="small text-info">${feature.properties.intensity}</div>` : ''}
            </div>
          `);
        }
      }
    }).addTo(cycloneLayerGroup);
  }

  // 5. Plot Buoy Stations
  if (stations && conditions) {
    stations.forEach(st => {
      const cond = conditions[st.slug];
      if (!cond) return;

      const isSafe = cond.safety_status === 'SAFE';
      const isDanger = cond.safety_status === 'UNSAFE';
      const markerColor = isDanger ? '#ff6b6b' : (isSafe ? '#1dd1a1' : '#feca57');

      const buoyIcon = L.divIcon({
        className: 'custom-buoy-marker',
        html: `
          <div style="position:relative; width:28px; height:28px; display:flex; align-items:center; justify-content:center;">
            <div style="position:absolute; width:28px; height:28px; border-radius:50%; background:${markerColor}; opacity:0.3; animation: pulse-danger 2s infinite;"></div>
            <div style="width:14px; height:14px; border-radius:50%; background:${markerColor}; border:2px solid #ffffff; box-shadow:0 0 8px ${markerColor};"></div>
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const marker = L.marker([st.lat, st.lon], { icon: buoyIcon });

      const popupContent = `
        <div style="min-width: 230px; font-family: 'Segoe UI', sans-serif;">
          <div style="font-weight:700; font-size:1.05rem; color:#00f2fe; margin-bottom:4px;">
            ${st.name}
          </div>
          <div style="font-size:0.8rem; color:#8ba3c7; margin-bottom:8px;">
            Station: ${st.buoy_id} | Depth: ${st.depth_m}m
          </div>
          <div style="background:rgba(255,255,255,0.05); padding:8px; border-radius:6px; margin-bottom:8px; font-size:0.85rem;">
            <div>🌊 <strong>Wave Height:</strong> ${cond.wave_height}m (${cond.wave_status})</div>
            <div>💨 <strong>Wind:</strong> ${cond.wind_speed} kts (${cond.wind_direction})</div>
            <div>🌡️ <strong>SST:</strong> ${cond.sst}°C</div>
            <div>🌿 <strong>Chlorophyll:</strong> ${cond.chlorophyll} mg/m³</div>
            <div>⚠️ <strong>Risk Score:</strong> <span style="color:${markerColor}; font-weight:700;">${cond.risk_score}/100</span></div>
          </div>
          <div style="margin-bottom:8px; font-size:0.8rem; color:#d1e3ff;">
            ${cond.advisory}
          </div>
          <a href="/?station=${st.slug}" class="btn btn-sm btn-info text-dark w-100 fw-bold" style="font-size:0.75rem;">
            <i class="bi bi-speedometer2"></i> View Live Dashboard
          </a>
        </div>
      `;

      marker.bindPopup(popupContent);
      buoyLayerGroup.addLayer(marker);
    });
  }

  // 6. Plot Potential Fishing Zones (PFZ) Points
  if (pfzZones) {
    pfzZones.forEach(zone => {
      const pfzCircle = L.circle([zone.lat, zone.lon], {
        color: '#00d2d3',
        fillColor: '#00d2d3',
        fillOpacity: 0.20,
        weight: 1.5,
        dashArray: '4, 6',
        radius: 35000
      });

      const pfzIcon = L.divIcon({
        className: 'custom-pfz-marker',
        html: `<div style="background:#00d2d3; color:#06101e; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800; border:2px solid #fff; box-shadow:0 0 10px #00d2d3;">🐟</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const marker = L.marker([zone.lat, zone.lon], { icon: pfzIcon });
      const speciesHtml = zone.expected_species ? zone.expected_species.join(', ') : 'Pelagic shoals';
      const popupContent = `
        <div style="min-width: 230px; font-family: 'Segoe UI', sans-serif;">
          <div style="font-weight:700; font-size:1rem; color:#00d2d3; margin-bottom:2px;">
            ${zone.name}
          </div>
          <div style="font-size:0.75rem; color:#8ba3c7; margin-bottom:6px;">
            ${zone.coast} Coast &bull; Productivity: <span class="text-success fw-bold">${zone.productivity_score}/100</span>
          </div>
          <div style="font-size:0.85rem; margin-bottom:6px;">
            <div>🌿 <strong>Chlorophyll:</strong> ${zone.chlorophyll}</div>
            <div>🌡️ <strong>SST Front:</strong> ${zone.sst_gradient}</div>
            <div>🐟 <strong>Target:</strong> ${speciesHtml}</div>
          </div>
          <div class="badge bg-success bg-opacity-25 text-success border border-success w-100 p-1">
            ${zone.fuel_saving_est}
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);
      pfzCircle.bindPopup(popupContent);

      pfzLayerGroup.addLayer(pfzCircle);
      pfzLayerGroup.addLayer(marker);
    });
  }

  // Setup Layer Toggle Listeners
  setupMapLayerToggles();
}

function setupMapLayerToggles() {
  const toggleMap = {
    'layer-toggle-pfz': pfzLayerGroup,
    'layer-toggle-chlorophyll': chlorophyllLayerGroup,
    'layer-toggle-sst': sstLayerGroup,
    'layer-toggle-cyclone': cycloneLayerGroup,
    'layer-toggle-boundary': maritimeBoundaryLayerGroup,
    'layer-toggle-buoys': buoyLayerGroup
  };

  Object.entries(toggleMap).forEach(([id, layerGroup]) => {
    const el = document.getElementById(id);
    if (el && layerGroup && mainMap) {
      el.addEventListener('change', (e) => {
        if (e.target.checked) mainMap.addLayer(layerGroup);
        else mainMap.removeLayer(layerGroup);
      });
    }
  });
}

/* --------------------------------------------------------------------------
   PFZ & Route Navigation Map with Fishing Heatmap & Alternative Routes
   -------------------------------------------------------------------------- */
let routeMap = null;
let safeRoutePolyline = null;
let riskyRoutePolyline = null;
let routeMarkers = [];
let heatmapCircles = [];
let routeHazardCircles = [];

function initRouteMapWithHeatmap(routeData, heatmapPoints) {
  const mapContainer = document.getElementById('route-map-container');
  if (!mapContainer || !routeData) return;

  routeMap = L.map('route-map-container', {
    center: [14.5, 75.5],
    zoom: 6
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; CartoDB | ORCA Route Intelligence',
    subdomains: 'abcd'
  }).addTo(routeMap);

  // 1. Draw Simulated Fishing Heatmap Circles
  if (heatmapPoints) {
    heatmapPoints.forEach(pt => {
      const lat = pt[0];
      const lon = pt[1];
      const intensity = pt[2];
      
      const radius = 25000 + (intensity * 25000);
      const circle = L.circle([lat, lon], {
        color: 'transparent',
        fillColor: '#00d2d3',
        fillOpacity: 0.12 * intensity,
        radius: radius
      }).addTo(routeMap);
      heatmapCircles.push(circle);
    });
  }

  renderRouteComparison(routeData);
}

function renderRouteComparison(routeData) {
  if (!routeMap || !routeData) return;

  // Clear previous route items
  if (safeRoutePolyline) routeMap.removeLayer(safeRoutePolyline);
  if (riskyRoutePolyline) routeMap.removeLayer(riskyRoutePolyline);
  routeMarkers.forEach(m => routeMap.removeLayer(m));
  routeHazardCircles.forEach(c => routeMap.removeLayer(c));
  routeMarkers = [];
  routeHazardCircles = [];

  // 1. Draw Recommended Safest Route (Solid Green / Cyan)
  const safeWps = routeData.safe_route_waypoints || routeData.waypoints || [];
  if (safeWps.length > 0) {
    const safeCoords = safeWps.map(wp => [wp.lat, wp.lon]);
    safeRoutePolyline = L.polyline(safeCoords, {
      color: '#1dd1a1',
      weight: 4,
      opacity: 0.9
    }).addTo(routeMap);

    safeRoutePolyline.bindTooltip('<strong>Recommended Safest Route</strong> (Optimized)', {
      sticky: true
    });

    safeWps.forEach((wp, idx) => {
      const isStart = idx === 0;
      const isEnd = idx === safeWps.length - 1;
      const marker = L.circleMarker([wp.lat, wp.lon], {
        radius: isStart || isEnd ? 8 : 6,
        fillColor: isStart ? '#00d2d3' : (isEnd ? '#1dd1a1' : '#2ed573'),
        color: '#fff',
        weight: 2,
        fillOpacity: 0.95
      }).addTo(routeMap);

      marker.bindPopup(`
        <div style="font-family:'Segoe UI', sans-serif;">
          <div class="badge bg-success mb-1">Safest Route Waypoint</div>
          <strong>${wp.name}</strong><br/>
          🌊 Wave: ${wp.wave_m}m | 💨 Wind: ${wp.wind_kt} kts<br/>
          <span class="badge ${wp.risk === 'High' ? 'bg-danger' : (wp.risk === 'Moderate' ? 'bg-warning text-dark' : 'bg-success')} mt-1">${wp.risk} Risk</span>
        </div>
      `);
      routeMarkers.push(marker);
    });
  }

  // 2. Draw Risky Direct Route (Dashed Red Line)
  const riskyWps = routeData.risky_direct_waypoints || [];
  if (riskyWps.length > 0) {
    const riskyCoords = riskyWps.map(wp => [wp.lat, wp.lon]);
    riskyRoutePolyline = L.polyline(riskyCoords, {
      color: '#ff6b6b',
      weight: 3,
      dashArray: '6, 6',
      opacity: 0.75
    }).addTo(routeMap);

    riskyRoutePolyline.bindTooltip('<strong>Risky Direct Corridor</strong> (Hazard Intersect)', {
      sticky: true
    });
  }

  // 3. Draw Hazards on Path
  if (routeData.hazards_on_path) {
    routeData.hazards_on_path.forEach(hz => {
      const circle = L.circle([hz.lat, hz.lon], {
        color: '#ee5253',
        fillColor: '#ee5253',
        fillOpacity: 0.25,
        radius: (hz.radius_km || 30) * 1000
      }).addTo(routeMap);

      circle.bindPopup(`<strong>Hazard: ${hz.name}</strong><br/>Type: ${hz.type}`);
      routeHazardCircles.push(circle);
    });
  }

  if (safeRoutePolyline) {
    routeMap.fitBounds(safeRoutePolyline.getBounds(), { padding: [50, 50] });
  }
}
