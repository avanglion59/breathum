import json

import plotly.graph_objs as go
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from plotly.offline import plot

from analyzer.models import Sensor, DataItem
from analyzer.views import main


@login_required
def sensor_view(request, sensor_id):
    current_sensor = Sensor.objects.get(id = sensor_id)
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    source_data = dict(
        date = list(map(lambda x: x['timestamp'], values.values('timestamp'))),
        data = list(map(lambda x: x['data'], values.values('data')))
    )

    hover = HoverTool(
        tooltips = [
            ('Date', '@x{%d-%m-%Y %H:%M:%S}'),
            ('Sensor Data', "@y{0.00}"),
        ],
        formatters = {
            'x': 'datetime',
        },
        mode = 'vline'
    )

    TOOLS = [hover, "xpan", "xwheel_zoom", "reset", "save"]

    plot = figure(title = current_sensor.title + ', ' + current_sensor.unit, x_axis_type = "datetime", tools = TOOLS)

    plot.line(source_data['date'], source_data['data'])

    device_grid = gridplot([[plot]], sizing_mode = 'stretch_both')
    script, div = components(device_grid, CDN)
    return render(request, 'plotting.html', {'script': script, 'div': div})


@login_required
def plotly_sensor_view(request, sensor_id):
    current_sensor = Sensor.objects.get(id = sensor_id)
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    scatter1 = go.Scatter(
        x = list(map(lambda x: x['timestamp'], values.values('timestamp'))),
        y = list(map(lambda x: x['data'], values.values('data'))),
        name = 'Original',
        line = dict(
            shape = 'line'
        ),
        error_y = dict(
            type = 'constant',
            value = 50,
            visible = True
        )
    )

    scatter2 = go.Scatter(
        x = list(map(lambda x: x['timestamp'], values.values('timestamp'))),
        y = list(map(lambda x: x['data'], values.values('data'))),
        name = 'Convolved',
        line = dict(
            shape = 'spline'
        ),
    )

    div = plot(
        {
            'data': [scatter1, scatter2],
            'layout': go.Layout(
                title = current_sensor.title + ', ' + current_sensor.unit,
                autosize = True,
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = current_sensor.unit),
                plot_bgcolor = "#f0f1f3",
                paper_bgcolor = "#f0f1f3",
                showlegend = True,
                dragmode = 'pan'
            ),
        },
        output_type = 'div',
    )
    return render(request, 'plotting.html', {'script': '', 'div': div})


@login_required
def chartjs_sensor_view(request, sensor_id):
    current_sensor = Sensor.objects.get(id = sensor_id)
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    dates = json.dumps(list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp'))))
    data = json.dumps(list(map(lambda x: x['data'], values.values('data'))))
    label = current_sensor.title + ', ' + current_sensor.unit

    return render(request, 'chart.html', {'dates': dates, 'label': label, 'data': data, 'sensor': sensor_id})


def marker_api(request):
    current_sensor = Sensor.objects.get(id = request.GET.get('sensor_id'))
    attached_devices = Sensor.objects.filter(user__username = request.user)
    if current_sensor not in attached_devices:
        return redirect(main)

    values = DataItem.objects.filter(sensor = current_sensor).order_by('timestamp')

    dates = list(map(lambda x: x['timestamp'].isoformat(), values.values('timestamp')))
    data = list(map(lambda x: x['data'], values.values('data')))
    return JsonResponse({'labels': dates, 'data': data}, safe = False)
