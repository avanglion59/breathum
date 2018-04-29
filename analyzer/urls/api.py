from django.urls import path
from analyzer.views import map, sensor

urlpatterns = [
    path('map', map.APIMapView.as_view()),
    path('sensor', sensor.api),
]
