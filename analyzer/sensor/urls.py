from django.urls import path

from . import views

urlpatterns = [
    path('plotly/<uuid:sensor_id>/', views.plotly_sensor_view),
    path('<uuid:sensor_id>/', views.sensor_view),
    path('chart/<uuid:sensor_id>', views.chartjs_sensor_view),
    path('chart/markers', views.marker_api)
]
