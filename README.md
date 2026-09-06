# 🌊 ORCA – Ocean Risk & Condition Analyzer

**Smart India Hackathon (SIH) Prototype**

ORCA is a hydrodynamic and ocean risk surveillance web application built with **Django 5** and **Bootstrap 5**. Designed with a modern oceanic blue/teal theme, it provides real-time marine condition monitoring, early disaster warnings (Kallakkadal swell surges, squalls), INCOIS-style Potential Fishing Zones (PFZ), safe maritime route navigation, and conversational marine AI assistance.

---

## 🚀 Key Features & Pages

1. **Home Dashboard (`/`)**:
   - **Hero Section**: Live fleet telemetry counters (online buoys, operational sectors, active alerts, PFZ hotspots).
   - **Coastal Location Selector**: Live switcher across Indian maritime nodes (Mumbai, Kochi, Chennai, Visakhapatnam, Port Blair, Gujarat, Goa, Kavaratti/Lakshadweep, Paradip).
   - **Ocean Condition Cards**:
     - *Wave*: Significant Wave Height ($H_s$), swell height, swell period, direction.
     - *Wind*: Velocity in knots & km/h, gusts, Beaufort scale.
     - *SST*: Sea Surface Temperature (°C) and thermal anomaly.
     - *Tide*: Amplitude in meters, phase, next high/low tide predictions.
   - **Risk Score Gauge**: Visual canvas arc displaying 0–100 hydrodynamic composite risk score with dynamic color coding.
   - **Safe/Unsafe Status**: Operational directive with specific advisories for traditional crafts, motorized trawlers, and cargo ships.
   - **Mini Charts**: 24-hour rolling wave height and wind velocity trend lines (Chart.js).
   - **Quick AI Chatbot Launcher**: Floating action button + modal for rapid ocean intelligence.

2. **Ocean Map (`/map/`)**:
   - Interactive GIS marine map powered by **Leaflet.js** on dark oceanic basemaps.
   - Live buoy markers with pulsating radar rings & interactive telemetry popups.
   - Potential Fishing Zone (PFZ) chlorophyll bloom rings.
   - High-wave and swell hazard zone polygons with live layer toggle switches.

3. **AI Assistant (`/ai-assistant/`)**:
   - Conversational maritime NLP console (**ORCA DeepSea Intel**).
   - Domain-specific responses for wave surges, cyclone depressions, port-specific fishing safety, and nautical science.
   - One-click prompt chips and clear console controls.

4. **PFZ & Routes (`/pfz-routes/`)**:
   - **INCOIS-Style PFZ Advisories**: Chlorophyll-a density (mg/m³), SST thermal fronts, bearing, depth range, target species, and fuel savings estimates.
   - **Safe Route Navigation Planner**: Interactive route selection (e.g. Kochi → Lakshadweep, Mumbai → Gujarat Offshore, Chennai → Visakhapatnam), waypoint danger analysis, fuel optimization, and interactive route mapping.

5. **Alerts (`/alerts/`)**:
   - Maritime Early Warning System (MEWS) with severity filtering (Critical, Warning, Watch, Advisory, Normal).
   - Emergency audio siren simulator using the **Web Audio API** (no external audio files required).
   - Simulated fisherman SMS broadcast and marine VHF channel guide.

6. **Analytics (`/analytics/`)**:
   - Multi-day historical telemetry analysis powered by **Chart.js**:
     - 7-day Average vs Peak Wave Heights.
     - Sea Surface Temperature vs Climatological Baseline.
     - 7-day Risk Index Distribution.
   - Automated Hydrodynamic Anomaly Log tracking thermal spikes, tidal bore surges, and swell events.

---

## 🛠️ Project Structure

```
f:\ORAC\
├── manage.py
├── orca_project/
│   ├── settings.py           # Django 5 configuration (Static, Templates, Apps)
│   ├── urls.py               # Main URL router
│   ├── asgi.py
│   └── wsgi.py
├── analyzer/
│   ├── admin.py              # Model admin registrations
│   ├── apps.py
│   ├── models.py             # OceanStation, MarineCondition, OceanAlert, PFZZone, SafeRoute
│   ├── views.py              # Page views + REST-like JSON API endpoints
│   ├── urls.py               # App routing
│   ├── dummy_data.py         # Realistic Indian & global coastal marine datasets
│   ├── tests.py              # 11 automated unit tests
│   └── management/
│       └── commands/
│           └── seed_data.py  # Data populator command
├── templates/
│   ├── base.html             # Sticky topbar, collapsible sidebar, AI modal, siren audio
│   └── analyzer/
│       ├── home.html         # Dashboard, condition cards, gauge, mini charts
│       ├── map.html          # GIS surveillance map with Leaflet.js
│       ├── ai_assistant.html # Conversational AI interface
│       ├── pfz_routes.html   # PFZ advisories & safe route planner
│       ├── alerts.html       # Maritime Early Warning System
│       └── analytics.html    # Chart.js analytics & anomaly detection
└── static/
    ├── css/
    │   └── custom.css        # Modern oceanic blue/teal theme & animations
    ├── js/
    │   ├── main.js           # UI logic, sidebar toggle, IST clock, audio siren
    │   ├── charts.js         # Chart.js instances & canvas gauge
    │   └── ocean_map.js      # Leaflet GIS layers & route drawing
    └── images/
        └── orca_logo.svg     # Vector branding
```

---

## ⚙️ Running the Application

1. **Start the Django Development Server**:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

3. **Run Automated Tests**:
   ```bash
   python manage.py test
   ```

4. **Re-seed Sample Data** (if needed):
   ```bash
   python manage.py seed_data
   ```
