from django.contrib import admin

from .models.sensor import Sensor
from .models.data_item import DataItem
from .models.sensor_type import SensorType


class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


class DataItemAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'data', 'timestamp',)
    list_filter = ('sensor', 'timestamp',)
    readonly_fields = ('previous_hash',)


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'unit')
    list_filter = ('title',)


admin.site.register(DataItem, DataItemAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorType, SensorTypeAdmin)
