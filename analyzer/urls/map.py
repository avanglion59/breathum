from django.urls import path

from analyzer.views import map

urlpatterns = [
    path('point', map.PointMapView.as_view(), name ='pointmap'),
    path('heat', map.HeatMapView.as_view(), name ='heatmap'),
]
