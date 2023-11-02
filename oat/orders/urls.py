from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('orders/<year>/<month>/<day>/', views.orders_list, name='orders_list'),
    path(
        'department/<slug:slug>/',
        views.department_orders_list,
        name='department_orders_list',
    ),
    path('add/', views.order_add, name='order_add'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    # Редактирование заявки (реализация ???)
    path('<int:order_id>/edit/', views.order_edit, name='order_edit'),
    # Удаление заявки (реализовать закрытие отказом заказчика)
    path('delete/', views.order_delete, name='order_delete'),
    path('', views.home_page, name='home_page'),
]
