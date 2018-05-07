import random
import uuid
from datetime import datetime, timedelta
from hashlib import sha256

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import models


class SensorType(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    unit = models.CharField(max_length=30)

    # TODO: move this to SensorType model
    risk_bound = models.FloatField()
    danger_bound = models.FloatField()

    user = models.ManyToManyField(User)
    trust_level = models.DecimalField(max_digits=1, decimal_places=0)
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' (' + str(self.id) + ')'


class DataItem(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    data = models.FloatField()
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    previous_hash = models.TextField()

    @staticmethod
    def bootstrap_data(sensor_id, latitude=47.09514, longitude=37.54131, count=100):
        timestamp = datetime.now()
        for i in range(count):
            data = round(random.gauss(1000, 25))
            timestamp += timedelta(minutes=1)
            obj = DataItem(data=data, timestamp=timestamp, latitude=latitude, longitude=longitude,
                           sensor_id=sensor_id)
            obj.save()

    @staticmethod
    def blockchain_hash(obj):
        try:
            return sha256(serialize('json', [obj]).encode('utf-8')).hexdigest()
        except AttributeError:
            return 0

    @staticmethod
    def blockchain_verify():
        data_items = list(DataItem.objects.order_by('timestamp'))
        for n, i in enumerate(data_items):
            try:
                if DataItem.blockchain_hash(i) == data_items[n + 1].previous_hash:
                    continue
                else:
                    return DataItem.blockchain_hash(i), data_items[n + 1].previous_hash, False
            except IndexError:
                continue
        return True


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sensors = models.ManyToManyField(Sensor)
