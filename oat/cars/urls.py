from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_list'),
    path('column/<slug:slug>/', views.column_cars_list, name='column'),
    # Просмотр отдельной машины - СДЕЛАНО (доработать!)
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    # Добавление машины - СДЕЛАНО (редактировать форму)
    path('add/', views.car_add, name='car_add'),
    # Редактирование машины (возможно, нет...)
    path('<int:car_id>/edit/', views.car_edit, name='car_edit'),
    path('<int:car_id>/edit/delete/', views.car_delete, name='car_delete'),
]
