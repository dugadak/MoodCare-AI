from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceTokenViewSet,
    NotificationPreferenceViewSet,
    NotificationLogViewSet,
    NotificationViewSet
)

router = DefaultRouter()
router.register('tokens', DeviceTokenViewSet, basename='device-token')
router.register('preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register('logs', NotificationLogViewSet, basename='notification-log')
router.register('', NotificationViewSet, basename='notification')

app_name = 'notifications'
urlpatterns = [
    path('', include(router.urls)),
]