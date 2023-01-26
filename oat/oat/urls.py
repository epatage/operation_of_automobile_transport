from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('cars/', include('cars.urls', namespace='cars')),
    # path('', include('applications.urls', namespace='applications')),  # будет выводить главную страницу заявок
]
