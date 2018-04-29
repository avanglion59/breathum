from django.urls import path, include
from django.views.generic import TemplateView

from analyzer.views import general

urlpatterns = [
    path('', general.main, name='main'),
    path('insert', general.insert),
    path('logout', general.logout, name='logout'),
    path('map/', include('analyzer.urls.map')),
    path('sensor/', include('analyzer.urls.sensor')),
    path('dashboard', TemplateView.as_view(template_name='dashboard.html'))
]
