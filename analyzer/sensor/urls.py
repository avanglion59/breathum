from django.urls import path

from . import views

urlpatterns = [
    path('', views.sensor),
    path('api', views.api)
]
