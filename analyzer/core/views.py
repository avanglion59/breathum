import json
from datetime import datetime

from Crypto.Cipher import AES
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from analyzer.forms import LoginForm
from analyzer.models import DataItem


@csrf_exempt
def insert(request):
    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

        test_key = b'\x75\x37\x34\x72\x53\x76\x41\x6e\x4b\x46\x68\x55\x4e\x52\x55\x62' \
                   b'\x4c\x6f\x48\x69\x72\x31\x35\x71\x4d\x63\x45\x7a\x59\x7a\x6e\x51'

        # test_iv = b'\x9E\x7B\x98\x04\x41\x6D\xF6\xC7\x0E\x1C\xF3\x4E\x9F\x75\x2D\x08'

        iv = bytes.fromhex(request.POST.get('data')[:32])

        cyph = AES.new(test_key, AES.MODE_CBC, iv)

        decrypted = cyph.decrypt(bytes.fromhex(request.POST.get('data')[32:])).decode("ascii")

        data = json.loads(decrypted.replace(chr(0), ''))

        timestamp = datetime.now()

        item = DataItem(latitude=lat, longitude=lng, data=data['val'], timestamp=timestamp,
                        sensor_id=data['id'])
        item.save()

    elif request.method == 'GET':
        response.content = 'You must send POST queries!'

    return response


def main(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('map/point')
            else:
                return HttpResponseRedirect('/')
    return render(request, 'index.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
