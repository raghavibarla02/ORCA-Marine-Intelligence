from django.urls import path
from analyzer import views

urlpatterns = [
    # Main Application Pages
    path('', views.home_view, name='home'),
    path('map/', views.ocean_map_view, name='ocean_map'),
    path('ai-assistant/', views.ai_assistant_view, name='ai_assistant'),
    path('pfz-routes/', views.pfz_routes_view, name='pfz_routes'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('analytics/', views.analytics_view, name='analytics'),

    # API JSON Endpoints
    path('api/conditions/<slug:slug>/', views.api_condition_data, name='api_condition'),
    path('api/chat/', views.api_chat, name='api_chat'),
    path('api/routes/<str:route_key>/', views.api_route_details, name='api_route_details'),
    path('api/map-layers/', views.api_map_layers, name='api_map_layers'),
]
