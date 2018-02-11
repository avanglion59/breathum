import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from analyzer.models import Sensor, DataItem


def get_marker_data(request, user):
    host = request.get_host()

    url_base = 'https://' if request.is_secure() else 'http://' + host + '/sensor/chart/'

    sensors = Sensor.objects.filter(user__username = user)

    data = list()

    for sensor in sensors:
        val = DataItem.objects.filter(sensor = sensor).latest('timestamp')
        sensor_item = dict(
            lat = float(val.latitude),
            lng = float(val.longitude),
            val = val.data,
            desc = '<b>' + sensor.title + '</b>' + '<br>' +
                          str(sensor.type.title) + '<br>' +
                          sensor.unit + '<br>' +
                          str(val.data) + '<br>' +
                          '<a target="blank" href="' + url_base + str(sensor.id) + '">See Full Data</a>'
        )
        data.append(sensor_item)

    return data


def api(request):
    md = get_marker_data(request, request.user)
    return JsonResponse(md, safe = False)


@login_required
def map(request):
    md = get_marker_data(request, request.user)
    data = json.dumps(md)
    return render(request, 'map.html',
                  {'data': data,
                   'username': request.user.first_name + ' ' + request.user.last_name,
                   'email': request.user.email})
