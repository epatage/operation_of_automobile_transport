from django.urls import path, register_converter
from . import views
from .converters import DateConverter

app_name = 'applications'

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Стартовая страница

    path('all/', views.applications_list_, name='applications_list_all'),
    # Общий список заявок (сделать разбиение по дням паджинатором)
    path('all/<year>/<month>/<day>/', views.applications_list, name='applications_list'),
    # Список заявок по подразделениям (отдельные страницы)
    path(
        'department/<slug:slug>/',   # Создать модель цеховых подразделений
        views.department_applications_list,
        name='department',
    ),
    # Добавление заявки (сделать ссылку с главной страницы)
    path('add/', views.application_add, name='application_add'),

    # # Добавление заявки через formset классом
    # path('add/', views.ApplicationAddView.as_view(), name='application_add'),

    # Просмотр отдельной заявки (надо ли ???), туда добавить время подачи + инф.... нужно редактирование
    path('<int:application_id>/', views.application_detail, name='application_detail'),
    # Редактирование заявки (реализация ???)
    path('<int:application_id>/edit/', views.application_edit, name='application_edit'),
    # Удаление заявки (реализовать закрытие отказом заказчика)
    path('delete/', views.application_delete, name='application_delete'),
]
