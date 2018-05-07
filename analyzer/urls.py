from django.urls import path, include

from analyzer.core import views

urlpatterns = [
    path('', views.main, name='main'),
    path('insert', views.insert),
    path('logout', views.logout, name='logout'),
    path('map/', include('analyzer.maps.urls')),
    path('sensor/', include('analyzer.charts.urls')),
    path('api/', include('analyzer.api.urls')),
]
