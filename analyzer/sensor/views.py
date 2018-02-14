import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from analyzer.models import Sensor, DataItem
from analyzer.views import main


@login_required
def sensor(request):
    current_sensor = Sensor.objects.get(id = request.GET.get('id'))
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    dates = json.dumps(list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp'))))
    data = json.dumps(list(map(lambda x: x['data'], values.values('data'))))
    label = current_sensor.title + ', ' + current_sensor.unit

    return render(request, 'chart.html',
                  {'dates': dates, 'label': label, 'data': data, 'sensor': request.GET.get('id')})


@login_required
def api(request):
    current_sensor = Sensor.objects.get(id = request.GET.get('id'))
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    dates = list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp')))
    data = list(map(lambda x: x['data'], values.values('data')))
    return JsonResponse({'labels': dates, 'data': data}, safe = False)
