from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Column
from .forms import CarAddForm


# Общий список транспорта
@login_required
def cars_list(request):
    cars = Car.objects.all()
    cars_count = cars.count()

    context = {
        'cars': cars,
        'cars_count': cars_count,
    }

    return render(request, 'cars/cars_list.html', context)


# Просмотр информации об отдельной машине (возможно, редактирование??)
@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }

    return render(request, 'cars/car_detail.html', context)  # Шаблон надо править !!


# Добавление машины в список
@login_required
def car_add(request):
    form = CarAddForm(request.POST or None)
    if form.is_valid():
        car = form.save(commit=False)
        car.save()

        return redirect('cars:cars_list')

    return render(request, 'cars/car_add.html', {'form': form})


# Изменение описания машины
@login_required
def car_edit(request):

    context = {

    }

    return render(request, '', context)


# Удаление машины (из общего списка, индивидуальный просмотр или перенести в редактирование)
@login_required
def car_delete(request, car_id):

    context = {

    }

    return render(request, '', context)


# Автоколонна и закрепленный в ней список транспорта
@login_required
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
