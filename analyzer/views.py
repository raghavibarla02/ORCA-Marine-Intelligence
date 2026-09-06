import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from analyzer.dummy_data import (
    STATIONS,
    CONDITIONS,
    get_hourly_trends,
    ANALYTICS_DATA,
    ALERTS,
    PFZ_ZONES,
    PRECOMPUTED_ROUTES,
    AI_AGENT_PIPELINE,
    GEOJSON_LAYERS,
    FISHING_HEATMAP_POINTS,
    query_ai_enhanced
)


def home_view(request):
    """Home Dashboard view with Collaborative AI Agents pipeline & explainable recommendations."""
    station_slug = request.GET.get('station', 'mumbai').lower()
    if station_slug not in CONDITIONS:
        station_slug = 'mumbai'

    current_station = next((s for s in STATIONS if s['slug'] == station_slug), STATIONS[0])
    current_condition = CONDITIONS[station_slug]
    hourly_trend = get_hourly_trends(station_slug)

    safe_stations_count = sum(1 for c in CONDITIONS.values() if c['safety_status'] == 'SAFE')
    critical_alerts_count = sum(1 for a in ALERTS if a['severity'] == 'CRITICAL')

    context = {
        'page_title': 'Home Dashboard',
        'active_page': 'home',
        'stations': STATIONS,
        'current_station': current_station,
        'current_condition': current_condition,
        'hourly_trend_json': json.dumps(hourly_trend),
        'latest_alerts': ALERTS[:4],
        'total_stations': len(STATIONS),
        'safe_stations_count': safe_stations_count,
        'critical_alerts_count': critical_alerts_count,
        'pfz_count': len(PFZ_ZONES),
        'agent_pipeline': AI_AGENT_PIPELINE,
        'recommendation': current_condition.get('explainable_recommendation'),
    }
    return render(request, 'analyzer/home.html', context)


def ocean_map_view(request):
    """Ocean Map view with Leaflet GIS layers: PFZ, Chlorophyll, SST, Cyclone, Maritime Boundary."""
    context = {
        'page_title': 'Ocean GIS Surveillance Map',
        'active_page': 'map',
        'stations_json': json.dumps(STATIONS),
        'conditions_json': json.dumps(CONDITIONS),
        'pfz_json': json.dumps(PFZ_ZONES),
        'alerts_json': json.dumps(ALERTS),
        'geojson_layers_json': json.dumps(GEOJSON_LAYERS),
        'stations': STATIONS,
    }
    return render(request, 'analyzer/map.html', context)


def ai_assistant_view(request):
    """ChatGPT-style conversational interface with right-hand live evidence panel."""
    initial_station = 'mumbai'
    initial_condition = CONDITIONS[initial_station]

    sample_queries = [
        "Is Mumbai coast safe for fishing today?",
        "Explain the Kallakkadal swell warning in Kochi",
        "Where are the top Potential Fishing Zones (PFZ) right now?",
        "What is the safest navigation route from Kochi to Lakshadweep?",
        "Provide cyclone bulletin for Deep Depression BOB-04",
        "What are the ocean conditions off Visakhapatnam?",
    ]

    context = {
        'page_title': 'ORCA DeepSea AI Assistant',
        'active_page': 'ai_assistant',
        'sample_queries': sample_queries,
        'agent_pipeline': AI_AGENT_PIPELINE,
        'stations': STATIONS,
        'initial_condition': initial_condition,
        'initial_station': next(s for s in STATIONS if s['slug'] == initial_station),
        'conditions_json': json.dumps(CONDITIONS),
    }
    return render(request, 'analyzer/ai_assistant.html', context)


def pfz_routes_view(request):
    """PFZ with fishing heatmap, productivity scores & safest route visualization."""
    initial_route_key = request.GET.get('route', 'kochi_kavaratti')
    if initial_route_key not in PRECOMPUTED_ROUTES:
        initial_route_key = 'kochi_kavaratti'

    current_route = PRECOMPUTED_ROUTES[initial_route_key]

    context = {
        'page_title': 'Potential Fishing Zones & Safe Routes',
        'active_page': 'pfz_routes',
        'pfz_zones': PFZ_ZONES,
        'routes': PRECOMPUTED_ROUTES,
        'current_route': current_route,
        'current_route_json': json.dumps(current_route),
        'all_routes_json': json.dumps(PRECOMPUTED_ROUTES),
        'heatmap_points_json': json.dumps(FISHING_HEATMAP_POINTS),
    }
    return render(request, 'analyzer/pfz_routes.html', context)


def alerts_view(request):
    """Maritime Early Warning Center with High Waves, Lightning, Cyclone, Geofence alerts."""
    category_filter = request.GET.get('category', 'ALL').strip()
    severity_filter = request.GET.get('severity', 'ALL').upper()

    filtered_alerts = ALERTS
    if category_filter != 'ALL':
        filtered_alerts = [a for a in filtered_alerts if a.get('type', a.get('category')) == category_filter or a.get('category') == category_filter]
    if severity_filter != 'ALL':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]

    counts = {
        'high_waves': sum(1 for a in ALERTS if a.get('type') == 'High Waves'),
        'lightning': sum(1 for a in ALERTS if a.get('type') == 'Lightning'),
        'cyclone': sum(1 for a in ALERTS if a.get('type') == 'Cyclone'),
        'geofence': sum(1 for a in ALERTS if a.get('type') == 'Geofence warning'),
        'critical': sum(1 for a in ALERTS if a['severity'] == 'CRITICAL'),
        'warning': sum(1 for a in ALERTS if a['severity'] == 'WARNING'),
        'total': len(ALERTS)
    }

    context = {
        'page_title': 'Maritime Early Warning System & Alerts',
        'active_page': 'alerts',
        'alerts': filtered_alerts,
        'counts': counts,
        'selected_category': category_filter,
        'selected_severity': severity_filter,
    }
    return render(request, 'analyzer/alerts.html', context)


def analytics_view(request):
    """Deep Ocean Analytics including 7-day SST, Wind, Wave, and Chlorophyll trends."""
    context = {
        'page_title': 'Ocean Condition Analytics & Anomaly Detection',
        'active_page': 'analytics',
        'analytics_json': json.dumps(ANALYTICS_DATA),
        'anomalies': ANALYTICS_DATA['anomalies'],
    }
    return render(request, 'analyzer/analytics.html', context)


# ==========================================
# REST-LIKE JSON API ENDPOINTS
# ==========================================

@require_GET
def api_condition_data(request, slug):
    """Get live marine condition and 24h trends for a station."""
    if slug not in CONDITIONS:
        return JsonResponse({'error': 'Station not found'}, status=404)

    station_info = next((s for s in STATIONS if s['slug'] == slug), None)
    condition_data = CONDITIONS[slug]
    trend_data = get_hourly_trends(slug)

    return JsonResponse({
        'status': 'success',
        'station': station_info,
        'condition': condition_data,
        'trend': trend_data,
    })


@csrf_exempt
@require_POST
def api_chat(request):
    """ChatGPT-style conversational endpoint returning reply + live evidence data."""
    try:
        body = json.loads(request.body.decode('utf-8'))
        message = body.get('message', '').strip()
    except Exception:
        message = request.POST.get('message', '').strip()

    if not message:
        return JsonResponse({'error': 'No message provided'}, status=400)

    ai_result = query_ai_enhanced(message)
    return JsonResponse({
        'status': 'success',
        'query': message,
        'response': ai_result['reply'],
        'station_slug': ai_result['station_slug'],
        'evidence': ai_result['evidence'],
    })


@require_GET
def api_route_details(request, route_key):
    """Get route details, waypoints, and productivity score."""
    if route_key not in PRECOMPUTED_ROUTES:
        return JsonResponse({'error': 'Route not found'}, status=404)
    return JsonResponse({
        'status': 'success',
        'route': PRECOMPUTED_ROUTES[route_key]
    })


@require_GET
def api_map_layers(request):
    """Geo-data for buoys, PFZ zones, alert hazards, and GeoJSON boundaries."""
    return JsonResponse({
        'status': 'success',
        'stations': STATIONS,
        'conditions': CONDITIONS,
        'pfz': PFZ_ZONES,
        'alerts': ALERTS,
        'geojson_layers': GEOJSON_LAYERS,
        'heatmap_points': FISHING_HEATMAP_POINTS,
    })
