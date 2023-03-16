from rest_framework import viewsets

from applications.models import Application
from .serializers import ApplicationCreateSerializer, ApplicationCloseSerializer


class ApplicationCreateViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ApplicationCloseSerializer
        return ApplicationCreateSerializer

    # Делал для корректного вывода ГРЗ
    # def get_queryset(self):
    #     application_id = self.kwargs.get('application_id')
    #     new_queryset = Application.objects.filter(application_id=application_id)
    #     return new_queryset
