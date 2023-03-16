from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls', namespace='api')),  # API urls
    path('about/', include('about.urls', namespace='about')),
    path('cars/', include('cars.urls', namespace='cars')),
    path('', include('applications.urls', namespace='applications')),  # будет выводить главную страницу заявок
]


handler404 = 'core.views.page_not_found'

handler403 = 'core.views.csrf_failure'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
