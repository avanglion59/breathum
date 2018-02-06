from django.urls import path, include

from analyzer import views

urlpatterns = [
    path('', views.login),
    path('add', views.insert_data),
    path('logout', views.logout),
    path('map/', include('analyzer.map.urls')),
    path('sensor/', include('analyzer.sensor.urls')),
]
