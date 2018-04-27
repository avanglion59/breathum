import uuid

from django.contrib.auth.models import User
from django.db import models

from analyzer.models.sensor_type import SensorType


class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    unit = models.CharField(max_length=30)
    risk_bound = models.FloatField()
    danger_bound = models.FloatField()
    user = models.ManyToManyField(User)
    trust_level = models.DecimalField(max_digits=1, decimal_places=0)
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' (' + str(self.id) + ')'