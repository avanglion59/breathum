from django.urls import path

from analyzer.api import views

urlpatterns = [
    path('map', views.APIMapView.as_view()),
    path('timedelta', views.APITimeDeltaView.as_view()),
    path('sensors', views.APISensorsView.as_view()),
    path('edges', views.APIEdgesView.as_view())
]
