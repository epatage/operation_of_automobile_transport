from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderCreateViewSet
from django.urls import include, path

app_name = 'api'

router = DefaultRouter()

router.register('v1/orders', OrderCreateViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
