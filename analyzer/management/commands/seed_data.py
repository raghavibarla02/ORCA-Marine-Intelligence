from django.core.management.base import BaseCommand
from analyzer.models import OceanStation, MarineCondition, OceanAlert, PFZZone, SafeRoute
from analyzer.dummy_data import STATIONS, CONDITIONS, ALERTS, PFZ_ZONES, PRECOMPUTED_ROUTES


class Command(BaseCommand):
    help = "Seed database with initial sample oceanographic data for ORCA"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding ORCA sample marine data..."))

        # 1. Seed Stations & Conditions
        for st in STATIONS:
            station, created = OceanStation.objects.update_or_create(
                slug=st["slug"],
                defaults={
                    "name": st["name"],
                    "state": st["state"],
                    "region": st["region"],
                    "lat": st["lat"],
                    "lon": st["lon"],
                    "buoy_id": st["buoy_id"],
                    "depth_m": st["depth_m"],
                    "salinity_psu": st["salinity_psu"],
                    "visibility_nm": st["visibility_nm"],
                    "is_active": True,
                }
            )

            cond_data = CONDITIONS.get(st["slug"])
            if cond_data:
                MarineCondition.objects.update_or_create(
                    station=station,
                    defaults={
                        "wave_height": cond_data["wave_height"],
                        "wave_status": cond_data["wave_status"],
                        "swell_height": cond_data["swell_height"],
                        "swell_period": cond_data["swell_period"],
                        "wave_direction": cond_data["wave_direction"],
                        "wind_speed": cond_data["wind_speed"],
                        "wind_kmh": cond_data["wind_kmh"],
                        "wind_gust": cond_data["wind_gust"],
                        "wind_direction": cond_data["wind_direction"],
                        "beaufort_scale": cond_data["beaufort_scale"],
                        "sst": cond_data["sst"],
                        "sst_anomaly": cond_data["sst_anomaly"],
                        "tide_level": cond_data["tide_level"],
                        "tide_phase": cond_data["tide_phase"],
                        "next_high_tide": cond_data["next_high_tide"],
                        "next_low_tide": cond_data["next_low_tide"],
                        "risk_score": cond_data["risk_score"],
                        "safety_status": cond_data["safety_status"],
                        "safety_level_label": cond_data["safety_level_label"],
                        "status_color": cond_data["status_color"],
                        "advisory": cond_data["advisory"],
                    }
                )

        # 2. Seed Alerts
        for alt in ALERTS:
            OceanAlert.objects.update_or_create(
                alert_id=alt["id"],
                defaults={
                    "title": alt["title"],
                    "severity": alt["severity"],
                    "badge_class": alt["badge_class"],
                    "icon": alt["icon"],
                    "region": alt["region"],
                    "issued_at": alt["issued_at"],
                    "valid_until": alt["valid_until"],
                    "category": alt["category"],
                    "wave_height_expected": alt["wave_height_expected"],
                    "summary": alt["summary"],
                    "action_required": alt["action_required"],
                    "is_active": True,
                }
            )

        # 3. Seed PFZ Zones
        for pfz in PFZ_ZONES:
            PFZZone.objects.update_or_create(
                zone_id=pfz["id"],
                defaults={
                    "name": pfz["name"],
                    "coast": pfz["coast"],
                    "lat": pfz["lat"],
                    "lon": pfz["lon"],
                    "distance_km": pfz["distance_km"],
                    "bearing": pfz["bearing"],
                    "depth_range": pfz["depth_range"],
                    "sst_gradient": pfz["sst_gradient"],
                    "chlorophyll": pfz["chlorophyll"],
                    "expected_species": pfz["expected_species"],
                    "confidence_score": pfz["confidence_score"],
                    "validity": pfz["validity"],
                    "fuel_saving_est": pfz["fuel_saving_est"],
                    "status": pfz["status"],
                }
            )

        # 4. Seed Routes
        for r_key, route in PRECOMPUTED_ROUTES.items():
            SafeRoute.objects.update_or_create(
                key=route["key"],
                defaults={
                    "origin": route["origin"],
                    "origin_slug": route["origin_slug"],
                    "destination": route["destination"],
                    "destination_slug": route["destination_slug"],
                    "distance_nm": route["distance_nm"],
                    "est_time_hours": route["est_time_hours"],
                    "safety_score": route["safety_score"],
                    "safety_status": route["safety_status"],
                    "status_badge": route["status_badge"],
                    "advisory": route["advisory"],
                    "fuel_efficiency": route["fuel_efficiency"],
                    "waypoints_data": route["waypoints"],
                    "hazards_data": route["hazards_on_path"],
                }
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded ORCA sample marine datasets!"))
