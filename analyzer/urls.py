from django.urls import path, include
from django.views.generic import TemplateView

from analyzer import views

urlpatterns = [
    path('', views.main, name='main'),
    path('insert', views.insert),
    path('logout', views.logout, name='logout'),
    path('map/', include('analyzer.map.urls')),
    path('sensor/', include('analyzer.sensor.urls')),
    path('dashboard', TemplateView.as_view(template_name='dashboard.html'))
]
