from django.urls import path, include

from analyzer import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('insert', views.insert),
    path('logout', views.logout, name = 'logout'),
    path('map/', include('analyzer.map.urls')),
    path('sensor/', include('analyzer.sensor.urls')),
]
