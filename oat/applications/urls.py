from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Общий список заявок (сделать разбиение по дням паджинатором)
    path('', views.applications_list, name='applications_list'),
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
