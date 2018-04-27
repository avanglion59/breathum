import random
from datetime import datetime, timedelta
from hashlib import sha256

from django.core.serializers import serialize
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from analyzer.models.sensor import Sensor


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
            data = round(random.gauss(750, 5))
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


@receiver(pre_save, sender=DataItem)
def blockchain_hasher(sender, instance, *args, **kwargs):
    instance.previous_hash = sender.blockchain_hash(sender.objects.order_by('timestamp').last())