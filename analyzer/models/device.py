import uuid

from django.db import models

from analyzer.models.sensor import Sensor


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sensors = models.ManyToManyField(Sensor)