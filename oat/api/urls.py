from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderCreateViewSet

app_name = 'api'

router = DefaultRouter()

router.register('v1/orders', OrderCreateViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
