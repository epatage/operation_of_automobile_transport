from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_list'),  # Общий список транспорта - СДЕЛАНО
    path('column/<slug:slug>/', views.column_cars_list, name='column'),  # Список ТС по колоннам - СДЕЛАНО
    path('<int:car_id>/', views.car_detail, name='car_detail'),  # Просмотр отдельной машины - СДЕЛАНО (доработать!)
    path('add/', views.car_add, name='car_add'),  # Добавление машины - СДЕЛАНО (редактировать форму)
    path('<int:car_id>/edit/', views.car_edit, name='car_edit'),  # Редактирование машины (возможно, нет...)
    path('<int:car_id>/edit/delete/', views.car_delete, name='car_delete'),  # Удаление машины

]
