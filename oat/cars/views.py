from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Column
from .forms import CarAddForm, CarEditForm
import pandas as pd


@login_required
def cars_list(request):
    """Общий список транспорта"""

    cars = Car.activated.select_related('type_car', 'column').all()
    cars_count = cars.count()
    df = pd.DataFrame(cars)

    context = {
        'cars': cars,
        'cars_count': cars_count,
        'df': df.to_html(),
    }

    return render(request, 'cars/cars_list.html', context)


@login_required
def car_detail(request, car_id):
    """Просмотр информации об отдельной машине"""

    car = get_object_or_404(Car, pk=car_id)

    return render(request, 'cars/car_detail.html', {'car': car})


@login_required
def car_add(request):
    """Добавление машины в список"""

    form = CarAddForm(request.POST or None)
    if form.is_valid():
        car = form.save(commit=False)
        car.save()

        return redirect('cars:cars_list')

    return render(request, 'cars/car_add.html', {'form': form})


@login_required
def car_edit(request, car_id):
    """Изменение описания машины"""

    car = get_object_or_404(Car, pk=car_id)
    form = CarEditForm(request.POST or None, instance=car)
    context = {'form': form, 'is_edit': True, 'car': car}
    if form.is_valid():
        form.save()

        return redirect('cars:car_detail', car_id=car.id)
    return render(request, 'cars/car_add.html', context)


@login_required
def car_delete(request, car_id):
    """Удаление машины"""

    #  сделать перенаправление со страницы редактирования машины
    car = get_object_or_404(Car, pk=car_id)
    car.delete()

    return redirect('cars:cars_list')


@login_required
def column_cars_list(request, slug):
    """Автоколонна и закрепленный в ней список транспорта"""

    column = get_object_or_404(Column, slug=slug)
    # Выборка только эксплуатируемых ТС
    cars = column.cars.filter(active=True)
    cars_count = cars.count()

    context = {
        'cars': cars,
        'column': column,
        'cars_count': cars_count,
    }

    return render(request, 'cars/column_cars_list.html', context)
