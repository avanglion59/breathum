from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import DataItem, Sensor, SensorType
from .serializers import UserSerializer, DataItemSerializer, SensorSerializer, SensorTypeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DataItemViewSet(viewsets.ModelViewSet):
    queryset = DataItem.objects.all()
    serializer_class = DataItemSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorTypeViewSet(viewsets.ModelViewSet):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer
