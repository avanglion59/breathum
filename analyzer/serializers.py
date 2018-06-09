from django.contrib.auth.models import User
from rest_framework import serializers

from .models import DataItem, Sensor, SensorType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'
