from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Column


# Общий список транспорта
def cars_list(request):
    cars = Car.objects.all()
    cars_count = cars.count()

    context = {
        'cars': cars,
        'cars_count': cars_count,
    }

    return render(request, 'cars/cars_list.html', context)


# Просмотр информации об отдельной машине (возможно, редактирование??)
def car_detail(request, car_id):

    context = {

    }

    return render(request, '', context)


# Добавление машины в список
def car_add(request):

    context = {

    }

    return render(request, '', context)


# Изменение описания машины
def car_edit(request):

    context = {

    }

    return render(request, '', context)


# Удаление машины (из общего списка, индивидуальный просмотр или перенести в редактирование)
def car_delete(request, car_id):

    context = {

    }

    return render(request, '', context)


# Автоколонна и закрепленный в ней список транспорта
def column_cars_list(request, slug):
    column = get_object_or_404(Column, slug=slug)
    cars = Car.objects.filter(column=column)
    cars_count = cars.count()

    context = {
        'cars': cars,
        'column': column,
        'cars_count': cars_count,
    }

    return render(request, 'cars/column_cars_list.html', context)
