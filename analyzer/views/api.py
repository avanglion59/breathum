from django.views import View
from abc import ABC, abstractmethod
from analyzer.models.sensor import Sensor
from analyzer.models.data_item import DataItem
from analyzer.models.sensor_type import SensorType
from django.http import JsonResponse
from datetime import date, timedelta


class APIView(ABC, View):
    @abstractmethod
    def get_data(self, request):
        pass

    @abstractmethod
    def get(self, request):
        pass


class APIMapView(APIView):
    def get_data(self, request):
        url_base = ('https://' if request.is_secure() else 'http://') + request.get_host() + '/sensor?id='

        sensors = Sensor.objects.filter(user__username=request.user)

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

    def get(self, request):
        data = self.get_data(request)
        return JsonResponse(data, safe=False)


class APITimeDeltaView(APIView):
    def get_data(self, request):
        current_sensor = Sensor.objects.get(id=request.GET.get('id'))

        if request.GET.get('from') != '' and request.GET.get('to') != '':
            start_date = [int(i) for i in request.GET.get('from').split('/')]
            end_date = [int(i) for i in request.GET.get('to').split('/')]

            start_date = date(start_date[2], start_date[1], start_date[0])
            end_date = date(end_date[2], end_date[1], end_date[0]) + timedelta(days=1)

            values = DataItem.objects.filter(sensor=current_sensor, timestamp__range=(start_date, end_date)).order_by(
                'timestamp')
        else:
            values = DataItem.objects.filter(sensor=current_sensor).order_by('timestamp')

        dates = list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp')))
        data = list(map(lambda x: x['data'], values.values('data')))

        return {'labels': dates, 'data': data, 'id': request.GET.get('id')}

    def get(self, request):
        current_sensor = Sensor.objects.get(id=request.GET.get('id'))
        attached_devices = Sensor.objects.filter(user__username=request.user)
        if current_sensor not in attached_devices:
            return JsonResponse({'response failed': 'not your sensor, bro'})
        else:
            return JsonResponse(self.get_data(request), safe=False)


class APISensorsView(APIView):
    def get_data(self, request):
        return [i.id for i in
                Sensor.objects.filter(user__username=request.user, type__title=request.GET.get('type'))]

    def get(self, request):
        return JsonResponse(self.get_data(request), safe=False)


class APIEdgesView(APIView):
    def get_data(self, request):
        sensor = Sensor.objects.filter(id=request.GET.get('id'))[0]
        return {'danger': sensor.danger_bound, 'risk': sensor.risk_bound}

    def get(self, request):
        current_sensor = Sensor.objects.get(id=request.GET.get('id'))
        attached_devices = Sensor.objects.filter(user__username=request.user)
        if current_sensor not in attached_devices:
            return JsonResponse({'response failed': 'not your sensor, bro'})
        else:
            return JsonResponse(self.get_data(request))
