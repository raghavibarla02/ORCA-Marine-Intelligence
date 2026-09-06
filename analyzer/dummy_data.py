"""
Dummy Marine & Oceanographic Dataset for ORCA (Ocean Risk & Condition Analyzer)
Prototype data modeled after INCOIS, IMD Marine Bulletins, and NOAA Ocean Data.
Includes Multi-Agent Collaborative Architecture, GeoJSON Maritime Layers,
Explainable AI Rationales, and Expanded Multi-Hazard Early Warnings.
"""

from datetime import datetime, timedelta
import math

# ==============================================================================
# 1. COLLABORATIVE AI AGENTS PIPELINE (Planner -> Marine -> Weather -> GIS -> ...)
# ==============================================================================
AI_AGENT_PIPELINE = [
    {
        "id": "agent-planner",
        "name": "Planner Agent",
        "short": "Planner",
        "icon": "bi-diagram-3-fill",
        "role": "Mission Orchestration & Query Decomposition",
        "status": "ONLINE",
        "badge_class": "info",
        "latency_ms": 14,
        "description": "Receives navigator queries, evaluates operational constraints, and coordinates downstream specialist agents."
    },
    {
        "id": "agent-marine",
        "name": "Marine Data Agent",
        "short": "Marine Data",
        "icon": "bi-water",
        "role": "Hydrodynamic Sensor Aggregator",
        "status": "ACTIVE",
        "badge_class": "primary",
        "latency_ms": 32,
        "description": "Ingests real-time buoy telemetry (AD06, BD11), wave height ($H_s$), swell spectra ($T_p$), and tidal levels."
    },
    {
        "id": "agent-weather",
        "name": "Weather Agent",
        "short": "Weather",
        "icon": "bi-cloud-lightning-rain-fill",
        "role": "Atmospheric & Lightning Tracker",
        "status": "ACTIVE",
        "badge_class": "warning",
        "latency_ms": 28,
        "description": "Monitors convective lightning clusters, squall lines, barometric troughs, and gale wind isotachs."
    },
    {
        "id": "agent-gis",
        "name": "GIS Spatial Agent",
        "short": "GIS",
        "icon": "bi-geo-alt-fill",
        "role": "Geospatial & Boundary Guard",
        "status": "ACTIVE",
        "badge_class": "info",
        "latency_ms": 45,
        "description": "Calculates 200 NM EEZ boundaries, territorial waters, bathymetry clearance, and maritime geofences."
    },
    {
        "id": "agent-analytics",
        "name": "Ocean Analytics Agent",
        "short": "Ocean Analytics",
        "icon": "bi-graph-up",
        "role": "Phytoplankton & Thermal Analyst",
        "status": "ONLINE",
        "badge_class": "success",
        "latency_ms": 50,
        "description": "Tracks Chlorophyll-a bloom fronts, SST gradients, upwelling eddies, and historical thermal anomalies."
    },
    {
        "id": "agent-risk",
        "name": "Risk Assessor Agent",
        "short": "Risk",
        "icon": "bi-shield-exclamation",
        "role": "Hydrodynamic Risk & Safety Engine",
        "status": "ACTIVE",
        "badge_class": "danger",
        "latency_ms": 22,
        "description": "Computes composite risk score (0-100), vessel capsize probability, and generates explainable rationales."
    },
    {
        "id": "agent-chat",
        "name": "Conversational Chat Agent",
        "short": "Chat",
        "icon": "bi-chat-dots-fill",
        "role": "Maritime Natural Language Interface",
        "status": "ONLINE",
        "badge_class": "info",
        "latency_ms": 65,
        "description": "Synthesizes multi-agent evidence into human-interpretable captain briefings and fisherman advisories."
    }
]

# ==============================================================================
# 2. COASTAL STATIONS & HYDRODYNAMIC CONDITIONS
# ==============================================================================
STATIONS = [
    {
        "id": "mumbai",
        "name": "Mumbai Coast (Arabian Sea)",
        "slug": "mumbai",
        "state": "Maharashtra",
        "region": "West Coast",
        "lat": 18.9220,
        "lon": 72.8347,
        "buoy_id": "AD06-INCOIS",
        "depth_m": 42,
        "salinity_psu": 35.8,
        "visibility_nm": 8.5,
    },
    {
        "id": "kochi",
        "name": "Kochi Harbor & Offshore",
        "slug": "kochi",
        "state": "Kerala",
        "region": "Southwest Coast",
        "lat": 9.9312,
        "lon": 76.2673,
        "buoy_id": "CB02-NIOT",
        "depth_m": 35,
        "salinity_psu": 34.9,
        "visibility_nm": 7.0,
    },
    {
        "id": "chennai",
        "name": "Chennai Port (Bay of Bengal)",
        "slug": "chennai",
        "state": "Tamil Nadu",
        "region": "East Coast",
        "lat": 13.0827,
        "lon": 80.2707,
        "buoy_id": "BD11-INCOIS",
        "depth_m": 48,
        "salinity_psu": 34.2,
        "visibility_nm": 9.0,
    },
    {
        "id": "vizag",
        "name": "Visakhapatnam Deep Sea",
        "slug": "vizag",
        "state": "Andhra Pradesh",
        "region": "East Coast",
        "lat": 17.6868,
        "lon": 83.2185,
        "buoy_id": "BD09-INCOIS",
        "depth_m": 65,
        "salinity_psu": 33.7,
        "visibility_nm": 10.0,
    },
    {
        "id": "port-blair",
        "name": "Port Blair (Andaman Sea)",
        "slug": "port-blair",
        "state": "Andaman & Nicobar",
        "region": "Island Territory",
        "lat": 11.6234,
        "lon": 92.7265,
        "buoy_id": "AN03-NIOT",
        "depth_m": 85,
        "salinity_psu": 32.8,
        "visibility_nm": 12.0,
    },
    {
        "id": "gujarat",
        "name": "Okha & Gujarat Offshore",
        "slug": "gujarat",
        "state": "Gujarat",
        "region": "Northwest Coast",
        "lat": 22.4667,
        "lon": 69.0667,
        "buoy_id": "AD02-INCOIS",
        "depth_m": 30,
        "salinity_psu": 36.5,
        "visibility_nm": 6.5,
    },
    {
        "id": "goa",
        "name": "Goa / Mormugao Anchorage",
        "slug": "goa",
        "state": "Goa",
        "region": "Central West Coast",
        "lat": 15.4100,
        "lon": 73.8000,
        "buoy_id": "CB04-NIOT",
        "depth_m": 28,
        "salinity_psu": 35.1,
        "visibility_nm": 8.0,
    },
    {
        "id": "kavaratti",
        "name": "Kavaratti (Lakshadweep)",
        "slug": "kavaratti",
        "state": "Lakshadweep",
        "region": "Island Territory",
        "lat": 10.5667,
        "lon": 72.6417,
        "buoy_id": "LK01-INCOIS",
        "depth_m": 120,
        "salinity_psu": 35.5,
        "visibility_nm": 14.0,
    },
    {
        "id": "paradip",
        "name": "Paradip Coastal Sector",
        "slug": "paradip",
        "state": "Odisha",
        "region": "East Coast",
        "lat": 20.3167,
        "lon": 86.6167,
        "buoy_id": "BD07-INCOIS",
        "depth_m": 52,
        "salinity_psu": 32.5,
        "visibility_nm": 7.5,
    }
]

CONDITIONS = {
    "mumbai": {
        "station_id": "mumbai",
        "wave_height": 1.4,
        "wave_unit": "m",
        "wave_status": "Slight to Moderate",
        "swell_height": 1.1,
        "swell_period": 9.2,
        "swell_period_unit": "s",
        "wave_direction": "WSW (245°)",
        "wind_speed": 12.5,
        "wind_unit": "knots",
        "wind_kmh": 23.2,
        "wind_gust": 17.0,
        "wind_direction": "SW (230°)",
        "beaufort_scale": "Force 4 (Moderate Breeze)",
        "sst": 29.4,
        "sst_unit": "°C",
        "sst_anomaly": "+0.5°C",
        "sst_status": "Favorable",
        "chlorophyll": 2.65,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 2.2,
        "tide_unit": "m",
        "tide_phase": "Flood Tide (Rising)",
        "next_high_tide": "14:10 IST (3.6m)",
        "next_low_tide": "20:30 IST (0.8m)",
        "risk_score": 28,
        "safety_status": "SAFE",
        "safety_level_label": "Safe to Venture",
        "status_color": "success",
        "lightning_risk": "Low (0 strikes in 60 NM)",
        "explainable_recommendation": {
            "headline": "Safe to venture into coastal and offshore sectors.",
            "rationale": "Safe to venture because wave height is low (1.4m), wind is moderate (12.5 kts), SST is favorable (29.4°C), and no convective lightning clusters are detected within 50 NM.",
            "factors": [
                {"factor": "Wave Height", "impact": "Positive (Low 1.4m)", "badge": "success"},
                {"factor": "Wind Velocity", "impact": "Normal (12.5 kt)", "badge": "success"},
                {"factor": "SST Fronts", "impact": "Favorable (29.4°C)", "badge": "success"},
                {"factor": "Lightning", "impact": "Zero Risk (Clear sky)", "badge": "success"},
                {"factor": "Geofence", "impact": "Clear of IMBL (>180 NM)", "badge": "success"}
            ]
        },
        "advisory": "Ocean conditions suitable for all mechanized vessels. Small traditional crafts safe to operate up to 20 nautical miles.",
        "barometric_pressure": 1011.5,
        "current_speed": 1.1,
        "current_dir": "NNW",
    },
    "kochi": {
        "station_id": "kochi",
        "wave_height": 3.7,
        "wave_unit": "m",
        "wave_status": "Rough Swell Surge",
        "swell_height": 3.3,
        "swell_period": 15.2,
        "swell_period_unit": "s",
        "wave_direction": "SW (220°)",
        "wind_speed": 28.5,
        "wind_unit": "knots",
        "wind_kmh": 52.8,
        "wind_gust": 39.0,
        "wind_direction": "WSW (240°)",
        "beaufort_scale": "Force 7 (Near Gale)",
        "sst": 28.1,
        "sst_unit": "°C",
        "sst_anomaly": "-0.4°C",
        "sst_status": "Upwelling",
        "chlorophyll": 3.40,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.5,
        "tide_unit": "m",
        "tide_phase": "High Slack",
        "next_high_tide": "11:45 IST (1.6m)",
        "next_low_tide": "18:20 IST (0.4m)",
        "risk_score": 86,
        "safety_status": "UNSAFE",
        "safety_level_label": "High Danger - Kallakkadal Swell Alert",
        "status_color": "danger",
        "lightning_risk": "Moderate (Convective squall line 15 NM SW)",
        "explainable_recommendation": {
            "headline": "Unsafe to venture: Critical Kallakkadal surge warning active.",
            "rationale": "Unsafe for all crafts off Kerala coast: Significant wave heights exceed 3.7m with long swell period (15.2s) causing catastrophic shore breaks and vessel capsizing risk, combined with near-gale gusts (39 kts).",
            "factors": [
                {"factor": "Wave Height", "impact": "Critical Danger (3.7m)", "badge": "danger"},
                {"factor": "Swell Period", "impact": "Long Period Surge (15.2s)", "badge": "danger"},
                {"factor": "Wind Gusts", "impact": "Squally (39.0 kt)", "badge": "warning"},
                {"factor": "Lightning", "impact": "Squall Line Active", "badge": "warning"},
                {"factor": "Shore Impact", "impact": "Severe Coastal Inundation", "badge": "danger"}
            ]
        },
        "advisory": "Total prohibition on artisanal and mechanized craft departures for 48 hours. Secure all berthed vessels firmly.",
        "barometric_pressure": 1005.2,
        "current_speed": 2.5,
        "current_dir": "South",
    },
    "chennai": {
        "station_id": "chennai",
        "wave_height": 1.1,
        "wave_unit": "m",
        "wave_status": "Calm to Slight",
        "swell_height": 0.8,
        "swell_period": 7.8,
        "swell_period_unit": "s",
        "wave_direction": "ESE (115°)",
        "wind_speed": 10.5,
        "wind_unit": "knots",
        "wind_kmh": 19.4,
        "wind_gust": 14.0,
        "wind_direction": "SE (135°)",
        "beaufort_scale": "Force 3 (Gentle Breeze)",
        "sst": 30.2,
        "sst_unit": "°C",
        "sst_anomaly": "+1.3°C",
        "sst_status": "Warm Anomaly",
        "chlorophyll": 2.10,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.0,
        "tide_unit": "m",
        "tide_phase": "Ebb Tide (Falling)",
        "next_high_tide": "16:05 IST (1.2m)",
        "next_low_tide": "22:15 IST (0.3m)",
        "risk_score": 18,
        "safety_status": "SAFE",
        "safety_level_label": "Prime Navigational Window",
        "status_color": "success",
        "lightning_risk": "Zero (Clear oceanic troposphere)",
        "explainable_recommendation": {
            "headline": "Highly favorable conditions for all commercial and fishing fleets.",
            "rationale": "Safe to venture because wave height is calm (1.1m), wind is gentle (10.5 kts), visibility exceeds 9 NM, and ocean surface temperatures are stable.",
            "factors": [
                {"factor": "Wave Height", "impact": "Calm (1.1m)", "badge": "success"},
                {"factor": "Wind Velocity", "impact": "Gentle (10.5 kt)", "badge": "success"},
                {"factor": "SST Fronts", "impact": "Warm (30.2°C)", "badge": "info"},
                {"factor": "Lightning", "impact": "Zero Activity", "badge": "success"},
                {"factor": "Visibility", "impact": "Excellent (9 NM)", "badge": "success"}
            ]
        },
        "advisory": "Optimal sea state for all marine operations, port pilotage, and offshore trawling.",
        "barometric_pressure": 1013.1,
        "current_speed": 0.7,
        "current_dir": "NE",
    },
    "vizag": {
        "station_id": "vizag",
        "wave_height": 2.5,
        "wave_unit": "m",
        "wave_status": "Moderate to Rough",
        "swell_height": 2.0,
        "swell_period": 11.4,
        "swell_period_unit": "s",
        "wave_direction": "S (185°)",
        "wind_speed": 21.0,
        "wind_unit": "knots",
        "wind_kmh": 38.9,
        "wind_gust": 28.0,
        "wind_direction": "SSW (200°)",
        "beaufort_scale": "Force 5 (Fresh Breeze)",
        "sst": 29.8,
        "sst_unit": "°C",
        "sst_anomaly": "+0.4°C",
        "sst_status": "Normal",
        "chlorophyll": 2.45,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.7,
        "tide_unit": "m",
        "tide_phase": "Rising Tide",
        "next_high_tide": "15:30 IST (1.9m)",
        "next_low_tide": "21:50 IST (0.5m)",
        "risk_score": 62,
        "safety_status": "MODERATE_RISK",
        "safety_level_label": "Small Craft Advisory",
        "status_color": "warning",
        "lightning_risk": "High (Active thunderstorm cells 35 NM ESE)",
        "explainable_recommendation": {
            "headline": "Moderate Risk: Small crafts exercise extreme caution.",
            "rationale": "Caution advised: While large vessels can navigate safely, small fishing boats face moderate wave chop (2.5m) and localized marine lightning clusters detected by Doppler radar.",
            "factors": [
                {"factor": "Wave Height", "impact": "Moderate (2.5m)", "badge": "warning"},
                {"factor": "Wind Velocity", "impact": "Fresh Breeze (21 kt)", "badge": "warning"},
                {"factor": "Lightning", "impact": "Active Storm Cells (High)", "badge": "danger"},
                {"factor": "Depression", "impact": "Trough 180 NM Offshore", "badge": "warning"}
            ]
        },
        "advisory": "Small motorized crafts remain within 12 NM of shore. Watch for sudden lightning squalls.",
        "barometric_pressure": 1007.8,
        "current_speed": 1.7,
        "current_dir": "ENE",
    },
    "port-blair": {
        "station_id": "port-blair",
        "wave_height": 2.8,
        "wave_unit": "m",
        "wave_status": "Rough Swell",
        "swell_height": 2.4,
        "swell_period": 12.5,
        "swell_period_unit": "s",
        "wave_direction": "SW (230°)",
        "wind_speed": 23.5,
        "wind_unit": "knots",
        "wind_kmh": 43.5,
        "wind_gust": 32.0,
        "wind_direction": "SW (225°)",
        "beaufort_scale": "Force 6 (Strong Breeze)",
        "sst": 30.8,
        "sst_unit": "°C",
        "sst_anomaly": "+1.8°C",
        "sst_status": "Thermal Heatwave",
        "chlorophyll": 1.85,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.8,
        "tide_unit": "m",
        "tide_phase": "High Tide",
        "next_high_tide": "12:10 IST (2.1m)",
        "next_low_tide": "18:40 IST (0.6m)",
        "risk_score": 68,
        "safety_status": "MODERATE_RISK",
        "safety_level_label": "Restricted Navigation Advisory",
        "status_color": "warning",
        "lightning_risk": "Moderate (Tropical cloud deck)",
        "explainable_recommendation": {
            "headline": "Restricted inter-island transit & coral bleaching watch.",
            "rationale": "High thermal anomaly (+1.8°C SST) triggering marine heatwave watch Level 1. Sea state exhibits choppy 2.8m waves requiring passenger ferry speed restrictions.",
            "factors": [
                {"factor": "SST Anomaly", "impact": "Heatwave Spike (+1.8°C)", "badge": "danger"},
                {"factor": "Wave Height", "impact": "Rough Swell (2.8m)", "badge": "warning"},
                {"factor": "Wind Velocity", "impact": "Strong Breeze (23.5 kt)", "badge": "warning"}
            ]
        },
        "advisory": "Speed restrictions on inter-island catamarans. Watersports suspended.",
        "barometric_pressure": 1007.0,
        "current_speed": 1.9,
        "current_dir": "North",
    },
    "gujarat": {
        "station_id": "gujarat",
        "wave_height": 2.0,
        "wave_unit": "m",
        "wave_status": "Moderate",
        "swell_height": 1.5,
        "swell_period": 9.5,
        "swell_period_unit": "s",
        "wave_direction": "WNW (290°)",
        "wind_speed": 20.5,
        "wind_unit": "knots",
        "wind_kmh": 38.0,
        "wind_gust": 27.0,
        "wind_direction": "NW (315°)",
        "beaufort_scale": "Force 5 (Fresh Breeze)",
        "sst": 27.9,
        "sst_unit": "°C",
        "sst_anomaly": "-0.1°C",
        "sst_status": "Normal",
        "chlorophyll": 2.95,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 4.1,
        "tide_unit": "m",
        "tide_phase": "Strong Ebb Tide",
        "next_high_tide": "13:40 IST (4.8m)",
        "next_low_tide": "20:00 IST (1.0m)",
        "risk_score": 54,
        "safety_status": "MODERATE_RISK",
        "safety_level_label": "High Tidal Bore Caution",
        "status_color": "warning",
        "lightning_risk": "Low (0 strikes in 40 NM)",
        "explainable_recommendation": {
            "headline": "Caution required in shallow tidal creeks and Gulf of Kutch.",
            "rationale": "Moderate conditions overall, but extreme tidal range (4.8m spring tide) creates hazardous cross-currents and risk of grounding on mudbanks.",
            "factors": [
                {"factor": "Tidal Bore", "impact": "Extreme Amplitude (4.8m)", "badge": "danger"},
                {"factor": "Wave Height", "impact": "Moderate (2.0m)", "badge": "warning"},
                {"factor": "Currents", "impact": "Strong Rip (3.1 kt)", "badge": "warning"}
            ]
        },
        "advisory": "Monitor tide tables strictly before navigation in Gulf channels.",
        "barometric_pressure": 1010.8,
        "current_speed": 3.1,
        "current_dir": "E",
    },
    "goa": {
        "station_id": "goa",
        "wave_height": 1.5,
        "wave_unit": "m",
        "wave_status": "Moderate",
        "swell_height": 1.2,
        "swell_period": 9.2,
        "swell_period_unit": "s",
        "wave_direction": "WSW (240°)",
        "wind_speed": 14.0,
        "wind_unit": "knots",
        "wind_kmh": 25.9,
        "wind_gust": 18.0,
        "wind_direction": "W (265°)",
        "beaufort_scale": "Force 4 (Moderate)",
        "sst": 29.1,
        "sst_unit": "°C",
        "sst_anomaly": "+0.3°C",
        "sst_status": "Normal",
        "chlorophyll": 2.70,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.7,
        "tide_unit": "m",
        "tide_phase": "Slack Water",
        "next_high_tide": "14:50 IST (2.0m)",
        "next_low_tide": "21:10 IST (0.6m)",
        "risk_score": 32,
        "safety_status": "SAFE",
        "safety_level_label": "Safe for Coastal Operations",
        "status_color": "success",
        "lightning_risk": "Low",
        "explainable_recommendation": {
            "headline": "Safe to venture for commercial and artisanal fishing.",
            "rationale": "Low wave chop (1.5m) and moderate 14 kt winds. Standard night watch and VHF listening watch advised.",
            "factors": [
                {"factor": "Wave Height", "impact": "Moderate (1.5m)", "badge": "success"},
                {"factor": "Wind Velocity", "impact": "Mild (14.0 kt)", "badge": "success"},
                {"factor": "Lightning", "impact": "Clear", "badge": "success"}
            ]
        },
        "advisory": "Waters favorable for trawler departures and coastal tourism.",
        "barometric_pressure": 1011.9,
        "current_speed": 1.0,
        "current_dir": "NW",
    },
    "kavaratti": {
        "station_id": "kavaratti",
        "wave_height": 3.9,
        "wave_unit": "m",
        "wave_status": "Oceanic Swell Alert",
        "swell_height": 3.5,
        "swell_period": 15.6,
        "swell_period_unit": "s",
        "wave_direction": "SW (225°)",
        "wind_speed": 29.5,
        "wind_unit": "knots",
        "wind_kmh": 54.6,
        "wind_gust": 41.0,
        "wind_direction": "SW (230°)",
        "beaufort_scale": "Force 7 (Near Gale)",
        "sst": 29.2,
        "sst_unit": "°C",
        "sst_anomaly": "+0.2°C",
        "sst_status": "Normal",
        "chlorophyll": 1.90,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 1.4,
        "tide_unit": "m",
        "tide_phase": "High Inflow",
        "next_high_tide": "12:00 IST (1.4m)",
        "next_low_tide": "18:10 IST (0.4m)",
        "risk_score": 90,
        "safety_status": "UNSAFE",
        "safety_level_label": "Critical Danger - Reef Breakers",
        "status_color": "danger",
        "lightning_risk": "Moderate",
        "explainable_recommendation": {
            "headline": "Critical Danger: Massive long-period swell breaking over atoll reefs.",
            "rationale": "High risk of capsize at lagoon passes. Oceanic swell height approaching 4.0m with 15.6s period. Small boat transfers strictly suspended.",
            "factors": [
                {"factor": "Wave Height", "impact": "Severe (3.9m)", "badge": "danger"},
                {"factor": "Swell Period", "impact": "Long Period (15.6s)", "badge": "danger"},
                {"factor": "Lagoon Passes", "impact": "Navigational Hazard", "badge": "danger"}
            ]
        },
        "advisory": "Lagoon passes closed to boat traffic. Severe breakers on western reefs.",
        "barometric_pressure": 1006.0,
        "current_speed": 2.9,
        "current_dir": "NE",
    },
    "paradip": {
        "station_id": "paradip",
        "wave_height": 1.7,
        "wave_unit": "m",
        "wave_status": "Moderate",
        "swell_height": 1.4,
        "swell_period": 9.8,
        "swell_period_unit": "s",
        "wave_direction": "S (175°)",
        "wind_speed": 16.5,
        "wind_unit": "knots",
        "wind_kmh": 30.6,
        "wind_gust": 22.0,
        "wind_direction": "SSW (205°)",
        "beaufort_scale": "Force 4-5 (Moderate)",
        "sst": 30.1,
        "sst_unit": "°C",
        "sst_anomaly": "+0.8°C",
        "sst_status": "Normal",
        "chlorophyll": 2.80,
        "chlorophyll_unit": "mg/m³",
        "tide_level": 2.1,
        "tide_unit": "m",
        "tide_phase": "Rising Tide",
        "next_high_tide": "15:10 IST (2.6m)",
        "next_low_tide": "21:30 IST (0.8m)",
        "risk_score": 38,
        "safety_status": "SAFE",
        "safety_level_label": "Normal Navigational Vigil",
        "status_color": "success",
        "lightning_risk": "Low",
        "explainable_recommendation": {
            "headline": "Safe for commercial cargo pilotage and deep-sea trawling.",
            "rationale": "Conditions normal across North Bay of Bengal sector. Wave heights stable at 1.7m with manageable 16.5 kt breeze.",
            "factors": [
                {"factor": "Wave Height", "impact": "Manageable (1.7m)", "badge": "success"},
                {"factor": "Wind Velocity", "impact": "Moderate (16.5 kt)", "badge": "success"},
                {"factor": "Visibility", "impact": "Clear (7.5 NM)", "badge": "success"}
            ]
        },
        "advisory": "Commercial cargo pilotage ongoing. Deep-sea fishing vessels cleared.",
        "barometric_pressure": 1009.8,
        "current_speed": 1.4,
        "current_dir": "NE",
    }
}

# 24-hour trends generator
def get_hourly_trends(station_slug):
    base = CONDITIONS.get(station_slug, CONDITIONS["mumbai"])
    base_wave = base["wave_height"]
    base_wind = base["wind_speed"]
    base_sst = base["sst"]
    base_chla = base["chlorophyll"]
    
    hours, waves, winds, ssts, chlas = [], [], [], [], []
    for i in range(24):
        hr_time = (datetime.now() - timedelta(hours=23-i)).strftime("%H:00")
        hours.append(hr_time)
        wave_var = math.sin(i / 3.0) * 0.35 + (i * 0.015)
        wind_var = math.cos(i / 2.5) * 2.8
        sst_var = math.sin(i / 4.0) * 0.25
        chla_var = math.cos(i / 3.5) * 0.2
        
        waves.append(round(max(0.4, base_wave + wave_var), 2))
        winds.append(round(max(4.0, base_wind + wind_var), 1))
        ssts.append(round(base_sst + sst_var, 1))
        chlas.append(round(max(1.0, base_chla + chla_var), 2))
        
    return {
        "labels": hours,
        "waves": waves,
        "winds": winds,
        "ssts": ssts,
        "chlorophyll": chlas,
    }

# ==============================================================================
# 3. 7-DAY ANALYTICS TRENDS (SST, Wind, Wave, Chlorophyll)
# ==============================================================================
ANALYTICS_DATA = {
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"],
    "wave_heights_avg": [1.4, 1.6, 2.1, 2.8, 3.2, 2.7, 2.2],
    "wave_heights_max": [1.9, 2.3, 2.9, 3.8, 4.2, 3.6, 3.1],
    "wind_speeds_avg": [12.4, 15.1, 19.3, 24.5, 27.2, 22.0, 18.4],
    "sst_trends": [28.9, 29.1, 29.3, 29.2, 29.0, 29.4, 29.6],
    "sst_baseline": [28.5, 28.5, 28.5, 28.5, 28.5, 28.5, 28.5],
    "chlorophyll_trends": [1.85, 2.10, 2.45, 2.90, 3.35, 2.80, 2.65],
    "chlorophyll_baseline": [1.50, 1.50, 1.50, 1.50, 1.50, 1.50, 1.50],
    "risk_index_history": [28, 35, 52, 76, 84, 69, 58],
    "anomalies": [
        {
            "date": "2026-09-04",
            "station": "Kochi Offshore",
            "parameter": "Significant Wave Surge",
            "observed": "3.8 m",
            "normal": "1.8 m",
            "severity": "CRITICAL",
            "cause": "Distant South Indian Ocean swell propagation"
        },
        {
            "date": "2026-09-05",
            "station": "Port Blair (Andaman)",
            "parameter": "Sea Surface Temperature Spike",
            "observed": "30.8 °C",
            "normal": "28.6 °C",
            "severity": "WARNING",
            "cause": "Prolonged low wind convergence / Marine heatwave"
        },
        {
            "date": "2026-09-03",
            "station": "Kavaratti (Lakshadweep)",
            "parameter": "Wind Gust Velocity",
            "observed": "42.0 knots",
            "normal": "18.0 knots",
            "severity": "CRITICAL",
            "cause": "Squall line transit over Arabian Sea"
        },
        {
            "date": "2026-09-02",
            "station": "Gujarat / Okha",
            "parameter": "Tidal Bore Amplitude",
            "observed": "+4.9 m",
            "normal": "+3.8 m",
            "severity": "WATCH",
            "cause": "Perigean spring tide alignment"
        }
    ]
}

# ==============================================================================
# 4. EXPANDED MARITIME ALERTS (High Waves, Lightning, Cyclone, Geofence)
# ==============================================================================
ALERTS = [
    {
        "id": "ALT-2026-0901",
        "title": "High Wave Alert (Kallakkadal / Swell Surge)",
        "type": "High Waves",
        "severity": "CRITICAL",
        "badge_class": "danger",
        "icon": "bi-tsunami",
        "region": "Kerala & Lakshadweep Coast",
        "stations_affected": ["kochi", "kavaratti"],
        "issued_at": "Today, 06:00 IST",
        "valid_until": "Tomorrow, 23:59 IST",
        "category": "High Wave / Swell",
        "wave_height_expected": "3.2m to 4.1m",
        "summary": "Rapid swell surge likely to inundate low-lying beaches and break over harbor breakwaters. Artisanal skiffs strictly prohibited.",
        "action_required": "Immediate suspension of small craft departures; secure shore-based fishing gear."
    },
    {
        "id": "ALT-2026-0902",
        "title": "Severe Marine Lightning & Convective Thunderstorms",
        "type": "Lightning",
        "severity": "WARNING",
        "badge_class": "warning",
        "icon": "bi-lightning-charge-fill",
        "region": "North Andhra Coast & Visakhapatnam Outer Sea",
        "stations_affected": ["vizag", "paradip"],
        "issued_at": "Today, 07:15 IST",
        "valid_until": "Next 12 Hours",
        "category": "Lightning",
        "wave_height_expected": "2.2m to 3.0m",
        "summary": "Intense lightning flash density (>45 strikes/min) detected across 35 NM offshore corridor with sudden squalls up to 65 km/h.",
        "action_required": "Lower vessel outriggers and whip antennas; seek shelter below deck during active strikes."
    },
    {
        "id": "ALT-2026-0903",
        "title": "Deep Depression / Cyclone Formation Watch (BOB-04)",
        "type": "Cyclone",
        "severity": "WARNING",
        "badge_class": "danger",
        "icon": "bi-tornado",
        "region": "East-Central Bay of Bengal",
        "stations_affected": ["port-blair", "vizag", "chennai"],
        "issued_at": "Today, 05:00 IST",
        "valid_until": "Valid for 72 Hours",
        "category": "Cyclone",
        "wave_height_expected": "3.5m to 5.0m",
        "summary": "Low-pressure system concentrated into Deep Depression, moving WNW at 14 km/h with central pressure 996 hPa. Likely to intensify into Cyclonic Storm.",
        "action_required": "All deep-sea fishing trawlers operating east of 88°E advised to return to nearest safe port."
    },
    {
        "id": "ALT-2026-0904",
        "title": "Geofence Violation Alert - IMBL Proximity Notice",
        "type": "Geofence warning",
        "severity": "CRITICAL",
        "badge_class": "danger",
        "icon": "bi-slash-circle-fill",
        "region": "Gulf of Mannar & Palk Bay Sector",
        "stations_affected": ["chennai"],
        "issued_at": "Today, 08:30 IST",
        "valid_until": "Continuous Active Geofence",
        "category": "Geofence warning",
        "wave_height_expected": "1.2m to 1.6m",
        "summary": "Automated radar telemetry detected 4 unmonitored fishing trawlers approaching within 2.5 NM of the International Maritime Boundary Line (IMBL).",
        "action_required": "Coast Guard VHF broadcast alert issued on Channel 16; vessels ordered to steer 270° West immediately."
    },
    {
        "id": "ALT-2026-0905",
        "title": "Perigean Spring Tide Channel Inundation",
        "type": "High Waves",
        "severity": "ADVISORY",
        "badge_class": "primary",
        "icon": "bi-water",
        "region": "Gulf of Kutch & Khambhat",
        "stations_affected": ["gujarat"],
        "issued_at": "Today, 08:00 IST",
        "valid_until": "Tomorrow, 14:00 IST",
        "category": "Tidal Surge",
        "wave_height_expected": "1.8m to 2.4m",
        "summary": "Abnormally high water levels during spring tide cycle (+4.8m). Risk of grounding on tidal flats during rapid ebb phase.",
        "action_required": "Coordinate vessel draft calculations before entering port channels."
    }
]

# ==============================================================================
# 5. POTENTIAL FISHING ZONES (PFZ) & FISHING HEATMAP DATA
# ==============================================================================
PFZ_ZONES = [
    {
        "id": "PFZ-IN-01",
        "name": "Kochi Offshore Front Sector 4",
        "coast": "Kerala",
        "lat": 9.7500,
        "lon": 75.8000,
        "distance_km": 38,
        "bearing": "245° WSW",
        "depth_range": "40 - 75 m",
        "sst_gradient": "27.8°C - 28.6°C (0.8°C front)",
        "chlorophyll": "3.25 mg/m³ (High Density)",
        "productivity_score": 94,
        "expected_species": ["Yellowfin Tuna", "Indian Mackerel", "Sardines", "Squid"],
        "confidence_score": "94%",
        "validity": "Valid till tomorrow 18:00 IST",
        "fuel_saving_est": "32% fuel savings",
        "status": "Optimal Yield",
        "density_rating": "Very High"
    },
    {
        "id": "PFZ-IN-02",
        "name": "Vizag Continental Shelf Sector B",
        "coast": "Andhra Pradesh",
        "lat": 17.4200,
        "lon": 83.5800,
        "distance_km": 46,
        "bearing": "130° SE",
        "depth_range": "60 - 110 m",
        "sst_gradient": "29.1°C - 29.9°C (0.8°C front)",
        "chlorophyll": "2.80 mg/m³ (Moderate-High)",
        "productivity_score": 88,
        "expected_species": ["Skipjack Tuna", "Ribbon Fish", "Carangids", "Shrimp"],
        "confidence_score": "88%",
        "validity": "Valid till tomorrow 20:00 IST",
        "fuel_saving_est": "28% fuel savings",
        "status": "Active Bloom",
        "density_rating": "High"
    },
    {
        "id": "PFZ-IN-03",
        "name": "Mumbai High Shelf Edge Alpha",
        "coast": "Maharashtra",
        "lat": 19.2500,
        "lon": 71.9000,
        "distance_km": 62,
        "bearing": "270° Due West",
        "depth_range": "50 - 90 m",
        "sst_gradient": "28.5°C - 29.3°C (0.8°C front)",
        "chlorophyll": "3.45 mg/m³ (Rich Bloom)",
        "productivity_score": 96,
        "expected_species": ["Silver Pomfret", "Bombay Duck", "Seer Fish", "Prawns"],
        "confidence_score": "96%",
        "validity": "Valid for next 48 Hours",
        "fuel_saving_est": "35% fuel savings",
        "status": "Prime Catch Sector",
        "density_rating": "Exceptional"
    },
    {
        "id": "PFZ-IN-04",
        "name": "Chennai Offshore Upwelling Eddy",
        "coast": "Tamil Nadu",
        "lat": 12.8500,
        "lon": 80.6500,
        "distance_km": 32,
        "bearing": "110° ESE",
        "depth_range": "45 - 80 m",
        "sst_gradient": "29.4°C - 30.2°C (0.8°C front)",
        "chlorophyll": "2.20 mg/m³ (Moderate)",
        "productivity_score": 82,
        "expected_species": ["Mackerel", "Tuna", "Snappers", "Cuttlefish"],
        "confidence_score": "85%",
        "validity": "Valid till tomorrow 12:00 IST",
        "fuel_saving_est": "25% fuel savings",
        "status": "Active",
        "density_rating": "Moderate"
    },
    {
        "id": "PFZ-IN-05",
        "name": "Okha Pelagic Trench",
        "coast": "Gujarat",
        "lat": 22.1000,
        "lon": 68.4500,
        "distance_km": 54,
        "bearing": "240° WSW",
        "depth_range": "35 - 70 m",
        "sst_gradient": "27.2°C - 28.0°C (0.8°C front)",
        "chlorophyll": "3.10 mg/m³ (High)",
        "productivity_score": 90,
        "expected_species": ["Hilsa", "Croakers", "Ribbon Fish", "Cephalopods"],
        "confidence_score": "91%",
        "validity": "Valid for next 36 Hours",
        "fuel_saving_est": "30% fuel savings",
        "status": "Active",
        "density_rating": "High"
    }
]

# Simulated Fishing Heatmap Point Clusters [lat, lon, intensity (0.0 to 1.0)]
FISHING_HEATMAP_POINTS = [
    [19.25, 71.90, 0.95],
    [19.30, 71.85, 0.90],
    [19.20, 71.95, 0.85],
    [19.10, 72.00, 0.70],
    [9.75, 75.80, 0.92],
    [9.80, 75.75, 0.88],
    [9.70, 75.85, 0.85],
    [9.65, 75.90, 0.65],
    [17.42, 83.58, 0.88],
    [17.45, 83.62, 0.82],
    [17.38, 83.50, 0.78],
    [12.85, 80.65, 0.80],
    [12.90, 80.70, 0.75],
    [22.10, 68.45, 0.90],
    [22.15, 68.50, 0.85],
    [15.35, 73.65, 0.72],
    [11.50, 92.60, 0.75],
]

# ==============================================================================
# 6. NAVIGATION ROUTE PLANNER (Safest Route vs Risky Route & Productivity)
# ==============================================================================
PRECOMPUTED_ROUTES = {
    "kochi_kavaratti": {
        "id": "route-01",
        "key": "kochi_kavaratti",
        "origin": "Kochi Harbor",
        "origin_slug": "kochi",
        "destination": "Kavaratti Island (Lakshadweep)",
        "destination_slug": "kavaratti",
        "distance_nm": 218,
        "est_time_hours": 14.5,
        "safety_score": 42,
        "safety_status": "HIGH_RISK",
        "status_badge": "danger",
        "productivity_score": 78,
        "advisory": "Route crosses severe swell convergence zone (>3.7m). Recommend postponing transit for 36 hours or adopting the Southern Lee Diversion corridor.",
        "fuel_efficiency": "Sub-optimal (Counter-currents & heavy head-seas)",
        "hazards_on_path": [
            {"name": "Kallakkadal Surge Hotspot", "lat": 10.15, "lon": 74.40, "radius_km": 45, "type": "Rough Swell (>3.6m)"},
            {"name": "Naval Exercise Sector Foxtrot", "lat": 9.80, "lon": 75.30, "radius_km": 20, "type": "Restricted Zone"}
        ],
        "safe_route_waypoints": [
            {"name": "WP1 - Kochi Fairway", "lat": 9.95, "lon": 76.20, "wave_m": 2.8, "wind_kt": 22, "risk": "Moderate"},
            {"name": "WP2 - South Lee Corridors", "lat": 9.30, "lon": 74.90, "wave_m": 2.4, "wind_kt": 18, "risk": "Low"},
            {"name": "WP3 - Suheli Channel Lee", "lat": 9.95, "lon": 73.20, "wave_m": 2.5, "wind_kt": 20, "risk": "Moderate"},
            {"name": "WP4 - Kavaratti Port", "lat": 10.56, "lon": 72.65, "wave_m": 2.9, "wind_kt": 24, "risk": "Moderate"}
        ],
        "risky_direct_waypoints": [
            {"name": "WP1 - Kochi Fairway", "lat": 9.95, "lon": 76.20, "wave_m": 2.8, "wind_kt": 22, "risk": "Moderate"},
            {"name": "WP2 - Mid-Channel Peak Swell", "lat": 10.20, "lon": 74.80, "wave_m": 3.8, "wind_kt": 30, "risk": "High"},
            {"name": "WP3 - Open Ridge", "lat": 10.45, "lon": 73.50, "wave_m": 3.5, "wind_kt": 28, "risk": "High"},
            {"name": "WP4 - Kavaratti Port", "lat": 10.56, "lon": 72.65, "wave_m": 2.9, "wind_kt": 24, "risk": "Moderate"}
        ]
    },
    "mumbai_gujarat": {
        "id": "route-02",
        "key": "mumbai_gujarat",
        "origin": "Mumbai Coast",
        "origin_slug": "mumbai",
        "destination": "Okha (Gujarat Offshore)",
        "destination_slug": "gujarat",
        "distance_nm": 285,
        "est_time_hours": 19.0,
        "safety_score": 86,
        "safety_status": "SAFE",
        "status_badge": "success",
        "productivity_score": 94,
        "advisory": "Optimal sailing conditions with trailing seas. Route traverses high-productivity fishing front off Saurashtra coast. Maintain clearance from Bombay High oil installations.",
        "fuel_efficiency": "Optimal (+14% fuel economy via following currents)",
        "hazards_on_path": [
            {"name": "Bombay High Offshore Exclusion", "lat": 19.40, "lon": 71.30, "radius_km": 30, "type": "Oil Infrastructure (500m CPA)"}
        ],
        "safe_route_waypoints": [
            {"name": "WP1 - Mumbai Pilot Station", "lat": 18.90, "lon": 72.75, "wave_m": 1.4, "wind_kt": 12, "risk": "Low"},
            {"name": "WP2 - Daman Offshore Corridor", "lat": 20.40, "lon": 72.10, "wave_m": 1.5, "wind_kt": 14, "risk": "Low"},
            {"name": "WP3 - Veraval Approach", "lat": 20.85, "lon": 70.30, "wave_m": 1.7, "wind_kt": 16, "risk": "Low"},
            {"name": "WP4 - Porbandar Transit", "lat": 21.60, "lon": 69.45, "wave_m": 1.8, "wind_kt": 18, "risk": "Low"},
            {"name": "WP5 - Okha Port Approach", "lat": 22.45, "lon": 69.05, "wave_m": 1.9, "wind_kt": 19, "risk": "Low"}
        ],
        "risky_direct_waypoints": [
            {"name": "WP1 - Mumbai Pilot Station", "lat": 18.90, "lon": 72.75, "wave_m": 1.4, "wind_kt": 12, "risk": "Low"},
            {"name": "WP2 - Direct Across Bombay High", "lat": 19.45, "lon": 71.25, "wave_m": 2.1, "wind_kt": 21, "risk": "High (Exclusion Zone)"},
            {"name": "WP3 - Shoal Ridge", "lat": 21.20, "lon": 69.80, "wave_m": 2.2, "wind_kt": 20, "risk": "Moderate"},
            {"name": "WP4 - Okha Port Approach", "lat": 22.45, "lon": 69.05, "wave_m": 1.9, "wind_kt": 19, "risk": "Low"}
        ]
    },
    "chennai_vizag": {
        "id": "route-03",
        "key": "chennai_vizag",
        "origin": "Chennai Port",
        "origin_slug": "chennai",
        "destination": "Visakhapatnam Deep Sea",
        "destination_slug": "vizag",
        "distance_nm": 330,
        "est_time_hours": 21.0,
        "safety_score": 76,
        "safety_status": "SAFE",
        "status_badge": "success",
        "productivity_score": 86,
        "advisory": "Coromandel sector favorable. Watch for localized thunderstorm cells as you approach Godavari Delta offshore waters.",
        "fuel_efficiency": "Good (Neutral current profile)",
        "hazards_on_path": [
            {"name": "Krishna-Godavari Drilling Field", "lat": 16.30, "lon": 82.20, "radius_km": 25, "type": "Gas Platforms"}
        ],
        "safe_route_waypoints": [
            {"name": "WP1 - Chennai Outer Anchorage", "lat": 13.12, "lon": 80.35, "wave_m": 1.1, "wind_kt": 10, "risk": "Low"},
            {"name": "WP2 - Nellore Safe Pass", "lat": 14.45, "lon": 80.20, "wave_m": 1.3, "wind_kt": 12, "risk": "Low"},
            {"name": "WP3 - Machilipatnam Offshore", "lat": 16.10, "lon": 81.30, "wave_m": 1.6, "wind_kt": 15, "risk": "Low"},
            {"name": "WP4 - Kakinada Deep Water Route", "lat": 16.90, "lon": 82.50, "wave_m": 2.0, "wind_kt": 18, "risk": "Moderate"},
            {"name": "WP5 - Visakhapatnam Breakwater", "lat": 17.67, "lon": 83.25, "wave_m": 2.2, "wind_kt": 18, "risk": "Moderate"}
        ],
        "risky_direct_waypoints": [
            {"name": "WP1 - Chennai Outer Anchorage", "lat": 13.12, "lon": 80.35, "wave_m": 1.1, "wind_kt": 10, "risk": "Low"},
            {"name": "WP2 - Inside KG Rig Zone", "lat": 16.30, "lon": 82.20, "wave_m": 2.4, "wind_kt": 22, "risk": "High (Restricted)"},
            {"name": "WP3 - Visakhapatnam Breakwater", "lat": 17.67, "lon": 83.25, "wave_m": 2.2, "wind_kt": 18, "risk": "Moderate"}
        ]
    }
}

# ==============================================================================
# 7. DUMMY GEOJSON MARITIME LAYERS (EEZ, Territorial, SST, Chlorophyll, Cyclone)
# ==============================================================================
GEOJSON_LAYERS = {
    # Indian Exclusive Economic Zone (200 NM Outer Limit line approximation)
    "maritime_boundaries": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Indian EEZ (200 NM Limit)", "type": "EEZ", "color": "#00f2fe", "dash": "6, 6"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [67.5, 23.5], [66.0, 20.0], [68.0, 16.0], [70.0, 11.0], [71.5, 7.5],
                        [75.0, 5.5], [77.5, 5.0], [80.5, 6.0], [85.0, 10.0], [88.5, 14.0],
                        [90.0, 18.0], [89.0, 21.0]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Territorial Waters (12 NM Limit)", "type": "Territorial", "color": "#1dd1a1", "dash": "3, 3"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [69.2, 22.8], [70.1, 21.0], [72.4, 19.2], [73.5, 16.0], [75.8, 10.5],
                        [77.4, 8.2], [78.5, 9.5], [80.3, 13.5], [82.5, 17.0], [86.5, 20.2]
                    ]
                }
            }
        ]
    },

    # Chlorophyll-a density bloom polygons (>2.5 mg/m³)
    "chlorophyll_blooms": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Mumbai Shelf Plankton Bloom", "chlorophyll": "3.45 mg/m³", "yield": "Exceptional", "color": "#00d2d3"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[71.3, 19.7], [72.4, 19.5], [72.2, 18.8], [71.2, 19.0], [71.3, 19.7]]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Kerala Upwelling Chlorophyll Front", "chlorophyll": "3.25 mg/m³", "yield": "High", "color": "#00d2d3"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[75.3, 10.2], [76.1, 10.0], [75.9, 9.3], [75.2, 9.5], [75.3, 10.2]]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Saurashtra Pelagic Plankton Zone", "chlorophyll": "3.10 mg/m³", "yield": "High", "color": "#00d2d3"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[68.1, 22.5], [69.0, 22.3], [68.8, 21.7], [68.0, 21.9], [68.1, 22.5]]]
                }
            }
        ]
    },

    # Sea Surface Temperature (SST) Thermal Fronts & Eddies
    "sst_fronts": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Coromandel Warm Core Eddy", "sst": "30.4 °C", "gradient": "+1.2 °C/10km", "color": "#ff9f43"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[81.0, 13.8], [82.0, 13.5], [81.8, 12.6], [80.8, 12.9], [81.0, 13.8]]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Southwest Coastal Cold Upwelling Filament", "sst": "27.8 °C", "gradient": "-1.4 °C/10km", "color": "#0abde3"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[75.0, 9.2], [75.6, 9.0], [75.4, 8.2], [74.8, 8.4], [75.0, 9.2]]]
                }
            }
        ]
    },

    # Active Cyclone Track & Forecast Cones (BOB-04 Deep Depression)
    "cyclone_track": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Cyclone BOB-04 Projected Track", "intensity": "Deep Depression -> Cyclonic Storm", "color": "#ee5253"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [91.5, 12.0], [89.8, 13.5], [88.0, 14.8], [86.2, 16.2], [84.8, 17.5]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Current Center (BOB-04)", "wind_speed": "55 km/h gusting 75 km/h", "pressure": "996 hPa"},
                "geometry": {"type": "Point", "coordinates": [89.8, 13.5]}
            },
            {
                "type": "Feature",
                "properties": {"name": "72h Uncertainty Forecast Cone", "color": "#ff6b6b"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[89.8, 13.5], [87.0, 16.5], [84.0, 19.0], [86.0, 19.5], [88.5, 16.0], [89.8, 13.5]]
                    ]
                }
            }
        ]
    }
}

# ==============================================================================
# 8. PRE-DEFINED CHATGPT-STYLE CONVERSATIONAL REPLIES (Multi-turn Support)
# ==============================================================================
CHAT_KNOWLEDGE = [
    {
        "keywords": ["mumbai", "safe", "fishing", "weather"],
        "station": "mumbai",
        "answer": """### 🌊 Mumbai Marine Safety Assessment

**Operational Recommendation:** **SAFE TO VENTURE**  
**Composite Risk Rating:** `28 / 100` (Low Hydrodynamic Risk)

---

#### 📊 Live Evidence Breakdown:
* **Significant Wave Height ($H_s$):** **1.4 m** (Calm to slight sea state)
* **Surface Wind:** **12.5 knots** from WSW (Force 4 Moderate Breeze)
* **Sea Surface Temperature:** **29.4 °C** (Normal, favorable thermal fronts)
* **Tide Status:** **+2.2 m** Flood tide; next high water at 14:10 IST (3.6m)
* **Marine Lightning:** **Zero activity** detected within 50 NM radius.

---

#### 💡 Explainable AI Rationale:
> **Safe to venture** because wave heights remain well below the 2.0m capsize safety threshold for small crafts, wind shear is gentle, and atmospheric barometric pressure is steady at **1011.5 hPa**. 

*Mechanized trawlers and artisanal crafts are cleared for operations up to 30 NM offshore.*"""
    },
    {
        "keywords": ["kochi", "kallakkadal", "surge", "safe", "kerala"],
        "station": "kochi",
        "answer": """### ⚠️ Kochi & Kerala Coast - Critical Swell Warning

**Operational Recommendation:** **STRICTLY UNSAFE - DO NOT VENTURE**  
**Composite Risk Rating:** `86 / 100` (High Danger)

---

#### 📊 Live Evidence Breakdown:
* **Significant Wave Height ($H_s$):** **3.7 m** (Rough sea state)
* **Peak Swell Period ($T_p$):** **15.2 seconds** (Long-period oceanic swell)
* **Surface Wind:** **28.5 knots**, with squall gusts reaching **39.0 knots**
* **Phenomenon:** **Kallakkadal (Swell Surge)** originating from distant southern ocean storms.

---

#### 💡 Explainable AI Rationale:
> **Unsafe to venture** because long-period swells (15.2s) travel with massive kinetic energy and steepen dramatically near shallow coastal banks, creating devastating breaking waves and strong rip currents. 

*Fishermen are strictly advised to suspend all sea trips for 48 hours and keep berthed vessels firmly anchored.*"""
    },
    {
        "keywords": ["pfz", "chlorophyll", "fish", "hotspot", "catch"],
        "station": "mumbai",
        "answer": """### 🐟 Potential Fishing Zones (PFZ) & Chlorophyll Hotspots

ORCA has synthesized high-resolution satellite **Ocean Colour Monitor (Chlorophyll-a)** and **SST thermal front** telemetry:

---

#### 🎯 Top 3 Validated High-Yield Spots Today:
1. **Mumbai High Shelf Edge Alpha** (62 km Due West, 270° bearing)
   * **Chlorophyll Bloom:** `3.45 mg/m³` (High density)
   * **Productivity Score:** **96 / 100** (Exceptional)
   * **Target Catch:** Silver Pomfret, Seer Fish, Squid, King Prawns
   * **Estimated Fuel Savings:** ~35% reduction in scouting time

2. **Kochi Offshore Front Sector 4** (38 km WSW, 245° bearing)
   * **Chlorophyll Bloom:** `3.25 mg/m³` | **Score:** **94 / 100**
   * **Target Catch:** Yellowfin Tuna, Indian Mackerel, Sardines

3. **Okha Pelagic Trench** (54 km WSW, 240° bearing)
   * **Chlorophyll Bloom:** `3.10 mg/m³` | **Score:** **90 / 100**
   * **Target Catch:** Hilsa, Croakers, Cephalopods

*Check the **PFZ & Routes** module to inspect the fishing heatmap and view safe approach routes.*"""
    },
    {
        "keywords": ["route", "kavaratti", "lakshadweep", "planner"],
        "station": "kochi",
        "answer": """### 🚢 Route Safety Analysis: Kochi Harbor → Kavaratti Island

* **Corridor Distance:** **218 Nautical Miles** (~14.5 hours steaming)
* **Direct Route Risk Rating:** `42 / 100` (High Hazard Corridor)

---

#### 🧭 Navigational Recommendation:
The direct rhumb line intersects the active **Kallakkadal swell convergence sector** between 73.5°E and 75.0°E, where wave heights exceed **3.8 meters**.

* **Recommended Alternative:** Steer south through the **Southern Lee Diversion Corridor** (via WP 9.30°N, 74.90°E) to maintain following seas and reduce rolling motion.
* **Productivity Note:** Expected fishing yield en route is **78/100**."""
    },
    {
        "keywords": ["cyclone", "storm", "depression", "bob"],
        "station": "vizag",
        "answer": """### 🌀 Cyclone Early Warning Bulletin: Deep Depression BOB-04

* **System Status:** Deep Depression over East-Central Bay of Bengal
* **Coordinates:** 13.5°N, 89.8°E (approx. 480 km ESE of Visakhapatnam)
* **Current Intensity:** Sustained winds **55 km/h**, gusting to **75 km/h**
* **Projected Track:** Moving WNW at 14 km/h; likely to intensify into Cyclonic Storm over next 24 hours.

---

#### 🚨 Protective Measures:
1. Signal **Local Cautionary Flag III** hoisted at Visakhapatnam and Paradip ports.
2. High swell surge advisory issued for coastal Andhra Pradesh.
3. Coastal fishermen out in deep waters should return to nearest harbor within 18 hours."""
    }
]

def query_ai_enhanced(user_prompt):
    """Conversational intelligence matcher with multi-agent context and station evidence."""
    cleaned = user_prompt.lower()
    
    best_item = None
    best_score = 0
    for item in CHAT_KNOWLEDGE:
        score = sum(1 for kw in item["keywords"] if kw in cleaned)
        if score > best_score:
            best_score = score
            best_item = item
            
    if best_item and best_score >= 1:
        station_slug = best_item.get("station", "mumbai")
        evidence = CONDITIONS.get(station_slug, CONDITIONS["mumbai"])
        return {
            "reply": best_item["answer"],
            "station_slug": station_slug,
            "evidence": evidence
        }
        
    for st in STATIONS:
        if st["slug"] in cleaned or st["name"].lower() in cleaned or st["state"].lower() in cleaned:
            cond = CONDITIONS.get(st["slug"], CONDITIONS["mumbai"])
            reply = f"""### 📊 Marine Telemetry for {st['name']}

**Operational Status:** **{cond['safety_status']}** (Risk Score: `{cond['risk_score']}/100`)

---

* **Significant Wave Height:** **{cond['wave_height']} m** ({cond['wave_status']})
* **Wind Velocity:** **{cond['wind_speed']} knots** ({cond['beaufort_scale']})
* **Sea Surface Temperature (SST):** **{cond['sst']} °C** ({cond['sst_anomaly']})
* **Chlorophyll-a:** **{cond['chlorophyll']} mg/m³**
* **Lightning Risk:** **{cond['lightning_risk']}**

---

#### 💡 Explainable AI Rationale:
> {cond['explainable_recommendation']['rationale']}

*Our multi-agent pipeline confirms all sensor links are synchronized.*"""
            return {
                "reply": reply,
                "station_slug": st["slug"],
                "evidence": cond
            }

    # Intelligent fallback
    evidence = CONDITIONS["mumbai"]
    reply = f"""### 🤖 ORCA Ocean Intelligence Response

I analyzed your query: **"{user_prompt}"** through our **Collaborative AI Agent Pipeline** (Planner → Marine → Weather → GIS → Analytics → Risk → Chat).

---

#### 🌊 Oceanwide Status Overview:
* **Active Buoy Nodes:** 9 Stations Reporting Live
* **High Swell Warning:** Active off Southwest Coast (Kochi & Lakshadweep)
* **Optimal Fishing Yield:** Mumbai High & Okha pelagic shelf (>3.0 mg/m³ chlorophyll)
* **Depression BOB-04:** Monitored over central Bay of Bengal

---

#### 💡 Try Asking:
* *"Is Mumbai coast safe for fishing today?"*
* *"Explain the Kallakkadal surge warning in Kochi"*
* *"Where are the top Potential Fishing Zones (PFZ) right now?"*
* *"What is the safest route from Kochi to Lakshadweep?"*"""
    return {
        "reply": reply,
        "station_slug": "mumbai",
        "evidence": evidence
    }
