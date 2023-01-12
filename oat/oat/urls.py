from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls', namespace='cars')),
    #path('', include('applications.urls')),  # будет вести на главную страницу заявок
]
