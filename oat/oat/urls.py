from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('cars/', include('cars.urls', namespace='cars')),
    #path('', include('applications.urls')),  # будет выводить главную страницу заявок
]
