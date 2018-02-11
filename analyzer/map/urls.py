from django.urls import path

from . import views

urlpatterns = [
    path('point', views.map, name = 'pointmap'),
    path('heat', views.map, name = 'heatmap'),
    path('api', views.api, name = 'api'),
]
