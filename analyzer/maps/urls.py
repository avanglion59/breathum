from django.urls import path

from analyzer.maps import views

urlpatterns = [
    path('point', views.PointMapView.as_view(), name='pointmap'),
    path('heat', views.HeatMapView.as_view(), name ='heatmap'),
]
