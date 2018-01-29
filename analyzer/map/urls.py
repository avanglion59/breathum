from django.urls import path

from . import views

urlpatterns = [
    path('', views.map_view),
    path('plotly', views.plotly_map_view)
]
