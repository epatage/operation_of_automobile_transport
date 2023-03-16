from . import views
from rest_framework.routers import DefaultRouter
from .views import ApplicationCreateViewSet
from django.urls import include, path

app_name = 'api'

router = DefaultRouter()

router.register('v1/applications', ApplicationCreateViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
