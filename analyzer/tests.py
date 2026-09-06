from django.test import TestCase, Client
from django.urls import reverse
import json


class ORCATestSuite(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ocean Risk &amp; Condition Analyzer")
        self.assertContains(response, "Significant Wave Height")
        # Verify Collaborative AI Agents pipeline & Explainable Recommendation
        self.assertContains(response, "Collaborative AI Agent Architecture Pipeline")
        self.assertContains(response, "Explainable AI Safety Decision Directive")

    def test_home_page_station_filter(self):
        response = self.client.get(reverse('home') + '?station=kochi')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kochi Harbor")
        self.assertContains(response, "Kallakkadal")

    def test_ocean_map_page(self):
        response = self.client.get(reverse('ocean_map'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ocean-map-container")
        # Verify layer toggle checkboxes
        self.assertContains(response, "layer-toggle-pfz")
        self.assertContains(response, "layer-toggle-chlorophyll")
        self.assertContains(response, "layer-toggle-sst")
        self.assertContains(response, "layer-toggle-cyclone")
        self.assertContains(response, "layer-toggle-boundary")

    def test_ai_assistant_page(self):
        response = self.client.get(reverse('ai_assistant'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ORCA DeepSea Intelligence Console")
        # Verify right evidence panel
        self.assertContains(response, "Live Evidence Inspection")
        self.assertContains(response, "COMPOSITE RISK SCORE")
        self.assertContains(response, "Significant Wave Height")

    def test_pfz_routes_page(self):
        response = self.client.get(reverse('pfz_routes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route-map-container")
        self.assertContains(response, "Pelagic Productivity Score")
        self.assertContains(response, "Recommended Safest Route")

    def test_alerts_page(self):
        response = self.client.get(reverse('alerts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maritime Early Warning System")
        # Verify expanded alert categories
        self.assertContains(response, "High Waves")
        self.assertContains(response, "Lightning")
        self.assertContains(response, "Cyclone")
        self.assertContains(response, "Geofence Warning")

    def test_alerts_filter_by_category(self):
        response = self.client.get(reverse('alerts') + '?category=Lightning')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Severe Marine Lightning")

    def test_analytics_page(self):
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        # Verify charts for SST, Wind, Wave, and Chlorophyll
        self.assertContains(response, "analyticsWaveChart")
        self.assertContains(response, "analyticsSstChart")
        self.assertContains(response, "analyticsWindChart")
        self.assertContains(response, "analyticsChlorophyllChart")

    def test_api_condition(self):
        response = self.client.get(reverse('api_condition', args=['mumbai']))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('condition', data)
        self.assertIn('trend', data)

    def test_api_chat_with_evidence(self):
        payload = json.dumps({'message': 'Is Mumbai safe for fishing?'})
        response = self.client.post(
            reverse('api_chat'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('Mumbai Marine Safety Assessment', data['response'])
        self.assertIn('evidence', data)
        self.assertEqual(data['evidence']['wave_height'], 1.4)

    def test_api_route_details(self):
        response = self.client.get(reverse('api_route_details', args=['kochi_kavaratti']))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['route']['distance_nm'], 218)
        self.assertIn('productivity_score', data['route'])

    def test_api_map_layers(self):
        response = self.client.get(reverse('api_map_layers'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('geojson_layers', data)
        self.assertIn('maritime_boundaries', data['geojson_layers'])
        self.assertIn('chlorophyll_blooms', data['geojson_layers'])
        self.assertIn('cyclone_track', data['geojson_layers'])
        self.assertIn('heatmap_points', data)
