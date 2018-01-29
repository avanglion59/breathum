import plotly.graph_objs as go
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, HoverTool, TapTool, ResetTool
)
from bokeh.resources import CDN
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from plotly.offline import plot

from analyzer.models import Sensor, DataItem

mapbox_access_token = 'pk.eyJ1IjoiYXZhbmdsaW9uNTkiLCJhIjoiY2pibDF6enpuNGc5dDJxcWdiZDRpcDU0bSJ9.BQztSi6LFVuqmISRRRiD9g'


def get_device_data(user):
    sensors = Sensor.objects.filter(user__username = user)

    data = list()

    for sensor in sensors:
        sensor_item = dict(
            type_title = sensor.type.title,
            unit = sensor.unit,
            sensor_title = sensor.title,
            sensor_id = sensor.id,
            value = DataItem.objects.filter(sensor = sensor).latest('timestamp')
        )
        data.append(sensor_item)

    return data


def add_map_data(map, sensor_data):
    print(sensor_data)
    source_data = dict(
        type_title = [i['type_title'] for i in sensor_data],
        sensor_title = [i['sensor_title'] for i in sensor_data],
        lat = [i['value'].latitude for i in sensor_data],
        lng = [i['value'].longitude for i in sensor_data],
        data = [i['value'].data for i in sensor_data]
    )
    source = ColumnDataSource(data = source_data)
    glyph = Circle(x = "lng", y = "lat", size = 15, fill_color = "blue", fill_alpha = 0.8, line_color = None)
    map.add_glyph(source, glyph)


@login_required
def map_view(request):
    data = get_device_data(request.user)

    # TODO: reassign latitiude and longitude to user's coordinates
    map_options = GMapOptions(lat = 47.12286, lng = 37.51542, map_type = "roadmap", zoom = 11)
    map = GMapPlot(x_range = Range1d(), y_range = Range1d(), map_options = map_options)

    map.api_key = 'AIzaSyCqSBoiiP3PHDlS7nNPx8 - uh44WOmdXQLI'
    add_map_data(map, data)

    hover = HoverTool(
        tooltips = [
            ("Type", "@type_title"),
            ("Title", "@sensor_title"),
            ("Sensor Data", "@data{0.00}"),
        ],
    )

    map.add_tools(PanTool(), WheelZoomTool(), hover, TapTool(), ResetTool())

    map_grid = gridplot([[map]], sizing_mode = 'stretch_both')

    script, div = components(map_grid, CDN)
    return render(request, 'plotting.html', {'script': script, 'div': div})


def make_hover_info(sensor, url_base):
    response = ''
    response += sensor['type_title'] + '<br>'
    response += sensor['unit'] + '<br>'
    response += str(sensor['value'].data) + '<br>'
    response += '<a href = "' + url_base + str(sensor['sensor_id']) + '">See Full Data</a>'
    return response

@login_required
def plotly_map_view(request):
    sensor_data = get_device_data(request.user)

    host = request.get_host()

    url_base = 'https://' if request.is_secure() else 'http://' + host + '/analyzer/sensor/plotly/'
    text_data = [make_hover_info(i, url_base) for i in sensor_data]

    data = go.Data([
        go.Scattermapbox(
            lat = [i['value'].latitude for i in sensor_data],
            lon = [i['value'].longitude for i in sensor_data],
            mode = 'markers',
            marker = go.Marker(
                size = 16,
                color = 'rgb(36, 115, 125)',
            ),
            text = text_data,
            hoverinfo = "text",
            hoverlabel = dict(
                bgcolor = 'rgb(248, 227, 244)'
            ),
            showlegend = False,
        )
    ])

    layout = go.Layout(
        title = 'Your Pollution Map',
        autosize = True,
        hovermode = 'closest',
        mapbox = dict(
            style = 'mapbox://styles/avanglion59/cjbl20qsu2s242spa3craz14j',
            accesstoken = mapbox_access_token,
            center = dict(
                lat = 47.12286,
                lon = 37.51542
            ),
        ),
        plot_bgcolor = "#f0f1f3",
        paper_bgcolor = "#f0f1f3",
    )

    fig = dict(data = data, layout = layout)
    div = plot(fig, output_type = 'div')
    return render(request, 'plotting.html', {'script': '', 'div': div})
