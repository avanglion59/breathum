from django.urls import path

from . import views

urlpatterns = [
    path('point', views.PointMapView.as_view(), name = 'pointmap'),
    path('heat', views.HeatMapView.as_view(), name = 'heatmap'),
    path('api', views.APIMapView.as_view(), name = 'api'),
]
