from django.db import models


class SensorType(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title