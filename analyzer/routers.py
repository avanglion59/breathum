from rest_framework import routers

from .viewsets import UserViewSet, DataItemViewSet, SensorTypeViewSet, SensorViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'dataitems', DataItemViewSet)
router.register(r'sensortypes', SensorTypeViewSet)
router.register(r'sensors', SensorViewSet)