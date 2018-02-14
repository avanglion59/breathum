from django.urls import path

from . import views

urlpatterns = [
    path('point', views.pointmap, name = 'pointmap'),
    path('heat', views.heatmap, name = 'heatmap'),
    path('api', views.api, name = 'api'),
]
