import json
from abc import ABC, abstractmethod

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from analyzer.models import DataItem, Sensor


@method_decorator(login_required, name='dispatch')
class MapView(ABC, View):
    def get_marker_data(self, request):
        host = request.get_host()

        url_base = ('https://' if request.is_secure() else 'http://') + host + '/sensor?id='

        sensors = Sensor.objects.filter(Q(user__username=request.user) | Q(shareable=True))

        data = list()

        for sensor in sensors:
            last_data_item = DataItem.objects.filter(sensor=sensor).latest('timestamp')
            condition = {}
            if last_data_item.data >= sensor.danger_bound:
                condition['color'] = 'red'
                condition['text'] = 'dangerous'
            elif last_data_item.data >= sensor.risk_bound:
                condition['color'] = 'orange'
                condition['text'] = 'risky'
            else:
                condition['color'] = 'green'
                condition['text'] = 'normal'
            sensor_item = dict(
                lat=float(last_data_item.latitude),
                lng=float(last_data_item.longitude),
                val=last_data_item.data,
                desc=f'<b>{sensor.title}</b><br>'
                     f'Type: {str(sensor.type.title)}<br>'
                     f'Last Data: {str(last_data_item.data)} {sensor.unit}<br>'
                     f'Air condition: <span style="color:{condition["color"]};">{condition["text"]}</span><br>'
                     f'<a target="_blank" href="https://goo.gl/Rm3Jiv">How to protect</a><br>'
                     f'<a target="_blank" href="{url_base}{str(sensor.id)}">See Full Data</a>'
            )
            data.append(sensor_item)

        return data

    @abstractmethod
    def get(self, request):
        pass


class PointMapView(MapView):
    template = 'analyzer/maps/pointmap.html'

    def get(self, request):
        marker_data = self.get_marker_data(request)
        data = json.dumps(marker_data)
        return render(request, self.template,
                      {'data': data,
                       'username': request.user.first_name + ' ' + request.user.last_name,
                       'email': request.user.email})


class HeatMapView(MapView):
    template = 'analyzer/maps/heatmap.html'

    def get(self, request):
        marker_data = self.get_marker_data(request)
        data = json.dumps(marker_data)
        return render(request, self.template,
                      {'data': data,
                       'username': request.user.first_name + ' ' + request.user.last_name,
                       'email': request.user.email})
