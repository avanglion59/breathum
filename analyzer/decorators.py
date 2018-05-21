from django.core.exceptions import PermissionDenied

from analyzer.models import Sensor


def user_is_sensor_owner(function):
    def wrap(request, *args, **kwargs):
        current_sensor = Sensor.objects.get(id=request.GET.get('id'))
        attached_devices = Sensor.objects.filter(user__username=request.user)
        if current_sensor in attached_devices or current_sensor.shareable:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
