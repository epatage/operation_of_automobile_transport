from django.urls import path, register_converter
from . import views
from .converters import DateConverter

app_name = 'orders'

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Стартовая страница

    path('all/', views.orders_list_, name='order_list_all'),  # Убрать/переписать ?
    # Общий список заявок (сделать разбиение по дням паджинатором)
    path('all/<year>/<month>/<day>/', views.orders_list, name='orders_list'),
    # Список заявок по подразделениям (отдельные страницы)
    path(
        'department/<slug:slug>/',   # Создать модель цеховых подразделений
        views.department_orders_list,
        name='department',
    ),
    # Добавление заявки (сделать ссылку с главной страницы)
    path('add/', views.order_add, name='order_add'),

    # # Добавление заявки через formset классом
    # path('add/', views.OrderAddView.as_view(), name='order_add'),

    # Просмотр отдельной заявки (надо ли ???), добавить время подачи + инф... нужно редактирование
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    # Редактирование заявки (реализация ???)
    path('<int:order_id>/edit/', views.order_edit, name='order_edit'),
    # Удаление заявки (реализовать закрытие отказом заказчика)
    path('delete/', views.order_delete, name='order_delete'),
]
