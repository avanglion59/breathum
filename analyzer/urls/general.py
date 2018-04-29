from django.urls import path, include

from analyzer.views import general

urlpatterns = [
    path('', general.main, name='main'),
    path('insert', general.insert),
    path('logout', general.logout, name='logout'),
    path('map/', include('analyzer.urls.map')),
    path('sensor/', include('analyzer.urls.sensor')),
    path('api/', include('analyzer.urls.api')),
]
