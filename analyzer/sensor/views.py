import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from analyzer.models import Sensor, DataItem
from analyzer.views import main


@login_required
def sensor(request):
    current_sensor = Sensor.objects.get(id=request.GET.get('id'))
    attached_devices = Sensor.objects.filter(user__username=request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor=current_sensor).order_by('timestamp')

    dates = json.dumps(list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp'))))
    data = json.dumps(list(map(lambda x: x['data'], values.values('data'))))
    label = current_sensor.title + ', ' + current_sensor.unit

    return render(request, 'chart.html',
                  {'dates': dates,
                   'label': label,
                   'data': data,
                   'sensor': request.GET.get('id'),
                   'type': current_sensor.type.title,
                   'risk': current_sensor.risk_bound,
                   'danger': current_sensor.danger_bound,
                   'trust': current_sensor.trust_level,
                   'unit': current_sensor.unit
                   })


@login_required
def api(request):
    current_sensor = Sensor.objects.get(id=request.GET.get('id'))
    attached_devices = Sensor.objects.filter(user__username=request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    if request.GET.get('from') != '' and request.GET.get('to') != '':
        start_date = [int(i) for i in request.GET.get('from').split('/')]
        end_date = [int(i) for i in request.GET.get('to').split('/')]

        start_date = date(start_date[2], start_date[1], start_date[0])
        end_date = date(end_date[2], end_date[1], 1 + end_date[0])

        values = DataItem.objects.filter(sensor=current_sensor, timestamp__range=(start_date, end_date)).order_by(
            'timestamp')
    else:
        values = DataItem.objects.filter(sensor=current_sensor).order_by('timestamp')

    dates = list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp')))
    data = list(map(lambda x: x['data'], values.values('data')))
    return JsonResponse({'labels': dates, 'data': data}, safe=False)
