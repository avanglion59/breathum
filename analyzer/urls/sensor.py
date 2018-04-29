from django.urls import path

from analyzer.views import sensor

urlpatterns = [
    path('', sensor.sensor),
    path('api', sensor.api)
]
