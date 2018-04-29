from django.views import View
from abc import ABC, abstractmethod
from analyzer.models.sensor import Sensor
from analyzer.models.data_item import DataItem


class APIView(ABC, View):
    @abstractmethod
    def get_data(self, is_secure, host, username):
        pass

    @abstractmethod
    def get(self):
        pass


class APIMapView(APIView):
    def get_data(self, is_secure, host, username):
        url_base = ('https://' if is_secure else 'http://') + host + '/sensor?id='

        sensors = Sensor.objects.filter(user__username=username)

        data = list()

        for sensor in sensors:
            last_data_item = DataItem.objects.filter(sensor=sensor).latest('timestamp')
            point_item = dict(
                lat=float(last_data_item.latitude),
                lng=float(last_data_item.longitude),
                val=last_data_item.data,
                desc=f'<b>{sensor.title}</b><br>'
                     f'{str(sensor.type.title)}<br>'
                     f'{sensor.unit}<br>'
                     f'{str(last_data_item.data)}<br>'
                     f'<a target="_blank" href="{url_base}{str(sensor.id)}">See Full Data</a>'
            )
            data.append(point_item)

        return data
