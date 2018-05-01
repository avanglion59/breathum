from django.urls import path
from analyzer.views import api

urlpatterns = [
    path('map', api.APIMapView.as_view()),
    path('timedelta', api.APITimeDeltaView.as_view()),
    path('sensors', api.APISensorsView.as_view()),
    path('edges', api.APIEdgesView.as_view())
]
