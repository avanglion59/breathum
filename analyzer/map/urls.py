from django.urls import path

from . import views

urlpatterns = [
    path('', views.map_view),
    path('plotly', views.plotly_map_view),
    path('ammap', views.ammap_map_view),
    path('markers', views.marker_api),
    path('gmaps', views.gmap)
]
