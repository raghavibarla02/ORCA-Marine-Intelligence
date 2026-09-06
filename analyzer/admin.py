from django.contrib import admin
from analyzer.models import OceanStation, MarineCondition, OceanAlert, PFZZone, SafeRoute


@admin.register(OceanStation)
class OceanStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'state', 'buoy_id', 'depth_m', 'is_active')
    search_fields = ('name', 'state', 'region', 'buoy_id')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MarineCondition)
class MarineConditionAdmin(admin.ModelAdmin):
    list_display = ('station', 'recorded_at', 'wave_height', 'wind_speed', 'sst', 'risk_score', 'safety_status')
    list_filter = ('safety_status', 'wave_status')


@admin.register(OceanAlert)
class OceanAlertAdmin(admin.ModelAdmin):
    list_display = ('alert_id', 'title', 'severity', 'region', 'category', 'is_active')
    list_filter = ('severity', 'category', 'is_active')


@admin.register(PFZZone)
class PFZZoneAdmin(admin.ModelAdmin):
    list_display = ('zone_id', 'name', 'coast', 'distance_km', 'confidence_score', 'status')
    list_filter = ('coast', 'status')


@admin.register(SafeRoute)
class SafeRouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance_nm', 'safety_score', 'safety_status')
    list_filter = ('safety_status',)
