from django.urls import path, include

from analyzer import views

urlpatterns = [
    path('', views.login),
    path('add', views.insert_data),
    path('login', views.login),
    path('logout', views.logout),
    path('map/', include('analyzer.map.urls')),
    path('sensor/', include('analyzer.sensor.urls')),
    path('api/', include('analyzer.api.urls')),
]
