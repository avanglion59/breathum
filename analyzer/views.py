import json
from datetime import datetime

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm
from .models import DataItem


@csrf_exempt
def insert_data(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        data = json.loads(request.POST.get('data'))
        timestamp = datetime.now()
        for i in data:
            item = DataItem(latitude = lat, longitude = lng, data = data[i], timestamp = timestamp, sensor_id = i)
            item.save()
    response = HttpResponse()
    response.status_code = 200
    return response


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'],
                                password = form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('map')
            else:
                return HttpResponseRedirect('login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('login')
