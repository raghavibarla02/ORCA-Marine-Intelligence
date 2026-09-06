from django.db import models


class OceanStation(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    buoy_id = models.CharField(max_length=50)
    depth_m = models.IntegerField(default=30)
    salinity_psu = models.FloatField(default=35.0)
    visibility_nm = models.FloatField(default=8.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.buoy_id})"


class MarineCondition(models.Model):
    station = models.ForeignKey(OceanStation, on_delete=models.CASCADE, related_name='conditions')
    recorded_at = models.DateTimeField(auto_now_add=True)
    wave_height = models.FloatField(help_text="Significant wave height in meters")
    wave_status = models.CharField(max_length=50, default="Moderate")
    swell_height = models.FloatField(default=1.0)
    swell_period = models.FloatField(help_text="Period in seconds")
    wave_direction = models.CharField(max_length=50)
    wind_speed = models.FloatField(help_text="Wind speed in knots")
    wind_kmh = models.FloatField()
    wind_gust = models.FloatField()
    wind_direction = models.CharField(max_length=50)
    beaufort_scale = models.CharField(max_length=100)
    sst = models.FloatField(help_text="Sea Surface Temperature in °C")
    sst_anomaly = models.CharField(max_length=50)
    tide_level = models.FloatField(help_text="Tide level in meters")
    tide_phase = models.CharField(max_length=100)
    next_high_tide = models.CharField(max_length=100)
    next_low_tide = models.CharField(max_length=100)
    risk_score = models.IntegerField(default=50)
    safety_status = models.CharField(max_length=50, default="SAFE")
    safety_level_label = models.CharField(max_length=150)
    status_color = models.CharField(max_length=20, default="success")
    advisory = models.TextField()

    def __str__(self):
        return f"{self.station.name} - Risk {self.risk_score} ({self.safety_status})"


class OceanAlert(models.Model):
    alert_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=50, choices=[
        ('CRITICAL', 'Critical'),
        ('WARNING', 'Warning'),
        ('WATCH', 'Watch'),
        ('ADVISORY', 'Advisory'),
        ('NORMAL', 'Normal'),
    ])
    badge_class = models.CharField(max_length=20, default="warning")
    icon = models.CharField(max_length=50, default="bi-exclamation-triangle")
    region = models.CharField(max_length=150)
    issued_at = models.CharField(max_length=100)
    valid_until = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    wave_height_expected = models.CharField(max_length=100)
    summary = models.TextField()
    action_required = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class PFZZone(models.Model):
    zone_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    coast = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    distance_km = models.IntegerField()
    bearing = models.CharField(max_length=50)
    depth_range = models.CharField(max_length=50)
    sst_gradient = models.CharField(max_length=100)
    chlorophyll = models.CharField(max_length=100)
    expected_species = models.JSONField(default=list)
    confidence_score = models.CharField(max_length=20)
    validity = models.CharField(max_length=100)
    fuel_saving_est = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return f"{self.name} ({self.coast})"


class SafeRoute(models.Model):
    key = models.CharField(max_length=100, unique=True)
    origin = models.CharField(max_length=150)
    origin_slug = models.CharField(max_length=100)
    destination = models.CharField(max_length=150)
    destination_slug = models.CharField(max_length=100)
    distance_nm = models.IntegerField()
    est_time_hours = models.FloatField()
    safety_score = models.IntegerField()
    safety_status = models.CharField(max_length=50)
    status_badge = models.CharField(max_length=20)
    advisory = models.TextField()
    fuel_efficiency = models.CharField(max_length=150)
    waypoints_data = models.JSONField(default=list)
    hazards_data = models.JSONField(default=list)

    def __str__(self):
        return f"{self.origin} to {self.destination}"
