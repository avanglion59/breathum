import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from analyzer.core.views import main
from analyzer.models import DataItem, Sensor, SensorType


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

    return render(request, 'analyzer/charts/chart.html',
                  {'dates': dates,
                   'label': label,
                   'data': data,
                   'sensor': request.GET.get('id'),
                   'type': current_sensor.type.title,
                   'risk': current_sensor.risk_bound,
                   'danger': current_sensor.danger_bound,
                   'trust': current_sensor.trust_level,
                   'unit': current_sensor.unit,
                   'category_list': SensorType.objects.all()
                   })
