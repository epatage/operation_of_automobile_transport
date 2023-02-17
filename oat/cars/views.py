from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Column
from .forms import CarAddForm, CarEditForm
import pandas as pd


# Общий список транспорта
@login_required
def cars_list(request):
    cars = Car.objects.all()
    cars_count = cars.count()
    df = pd.DataFrame(cars)

    context = {
        'cars': cars,
        'cars_count': cars_count,
        'df': df.to_html(),
    }

    return render(request, 'cars/cars_list.html', context)


# Просмотр информации об отдельной машине (отправка на редактирование)
@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    return render(request, 'cars/car_detail.html', {'car': car})


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
def car_edit(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    form = CarEditForm(request.POST or None, instance=car)
    context = {'form': form, 'is_edit': True, 'car': car}
    if form.is_valid():
        form.save()

        return redirect('cars:car_detail', car_id=car.id)
    return render(request, 'cars/car_add.html', context)


# Удаление машины
@login_required
def car_delete(request, car_id):
    #  сделать перенаправление со страницы редактирования машины
    car = get_object_or_404(Car, pk=car_id)
    car.delete()

    return redirect('cars:cars_list')


# Автоколонна и закрепленный в ней список транспорта
@login_required
def column_cars_list(request, slug):
    column = get_object_or_404(Column, slug=slug)
    cars = column.cars.all()  # Car.objects.filter(column=column)
    cars_count = cars.count()

    context = {
        'cars': cars,
        'column': column,
        'cars_count': cars_count,
    }

    return render(request, 'cars/column_cars_list.html', context)
