from django.urls import path
from django.views.generic import TemplateView
from .views import (
    get_coordinates, post_coordinates, getBuggyPosition, getUltrasonicDistance, 
    getDirection, getSmokeLevel, get_gas_sensor_value, webcam_image_view, 
    buggy_feed, get_detection
)

urlpatterns = [
    path('get-gas-sensor-value/', get_gas_sensor_value, name='get-gas-sensor-value'),
    path('get-coordinates/', get_coordinates, name='get-coordinates'),
    path('post-coordinates/', post_coordinates, name='post-coordinates'),
    path('getBuggyPosition/', getBuggyPosition, name='getBuggyPosition'),
    path('getUltrasonicDistance/', getUltrasonicDistance, name='getUltrasonicDistance'),
    path('getDirection/', getDirection, name='getDirection'),
    path('getSmokeLevel/', getSmokeLevel, name='getSmokeLevel'),
    path('webcam-image-view/', webcam_image_view, name='webcam-image-view'),
    path('buggy-feed/', buggy_feed, name='buggy-feed'),
    path('get-detection/', get_detection, name='get-detection'),
]
