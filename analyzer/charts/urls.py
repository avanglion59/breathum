from django.urls import path

from analyzer.charts import views

urlpatterns = [
    path('', views.sensor),
]
