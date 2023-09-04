from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Order, Department
from cars.models import TypeCar, Car
from .forms import DateForm, OrderAddForm, OrderEditForm, OrderAddFormSet, OrderCloseForm, OrderCloseFormSet
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.forms import modelformset_factory
import datetime
import time
from time import gmtime, strftime


def paginator(request, queryset):
    """Функция разделения (пагинации) заявок по датам."""
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {'page_obj': page_obj}


# Общий список заявок на главной странице
@login_required
def orders_list_(request):
    orders = Order.objects.all()

    departments = Department.objects.all()
    cars = Car.objects.all()

    if request.method == 'POST':
        formset = OrderCloseFormSet(request.POST, queryset=orders)
        if formset.is_valid():
            # for form in formset:
            #     form.save()
            # formset = formset.save(commit=False)  # возврат несохраненных полей
            formset.save()

    formset = OrderCloseFormSet(queryset=orders)
    context = {
        'orders': orders,
        'formset': formset,
        'is_edit': True,
        'departments': departments,
    }

    return render(request, 'orders/orders_list.html', context)


# Стартовая страница
@login_required
def home_page(request):
    dt_now = datetime.datetime.now()

    return redirect(
        'orders:orders_list',
        year=dt_now.year,
        month=dt_now.month,
        day=dt_now.day,
    )


# Общий список заявок на главной странице (по дням)
@login_required
def orders_list(request, year=None, month=None, day=None):
    # date = datetime.date(int(year), int(month), int(day))
    # show_date = date.strftime("%Y-%m-%d")
    # print(show_date, 'show_date')
    print('<------------')
    if not year or not month or not day:
        dt_now = datetime.datetime.now()

        print(dt_now)

    # departments = Department.objects.all()

    date = DateForm(request.GET or None, initial={'year': year, 'month': month, 'day': day}, prefix='date')

    if request.method == 'GET':
        if date.is_valid():
            year = date.cleaned_data['year']
            month = date.cleaned_data['month']
            day = date.cleaned_data['day']
        orders = Order.objects.filter(order_date__year=year, order_date__month=month, order_date__day=day)

        formset = OrderCloseFormSet(queryset=orders, prefix='order')
        context = {
            'orders': orders,
            'formset': formset,
            # 'departments': departments,
            'year': year,
            'month': month,
            'day': day,
            'date': date,
        }

        return render(request, 'orders/orders_list.html', context)

    orders = Order.objects.filter(order_date__year=year, order_date__month=month, order_date__day=day)

    if request.method == 'POST':
        formset = OrderCloseFormSet(request.POST or None, queryset=orders, prefix='order')
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                form.save()
            # formset = formset.save(commit=False)  # возврат несохраненных полей
            # formset.save()

    formset = OrderCloseFormSet(queryset=orders, prefix='order')
    context = {
        'orders': orders,
        'day': day,
        'month': month,
        'year': year,
        'formset': formset,
        'is_edit': True,
        # 'departments': departments,
        'date': date,
    }

    return render(request, 'orders/orders_list.html', context)

# Список заявок по цеховым подразделениям
@login_required
def department_orders_list(request, slug):
    department = get_object_or_404(Department, slug=slug)
    orders = department.orders.all()

    departments = Department.objects.all()

    formset = OrderCloseFormSet(queryset=orders)

    context = {
        # 'page_obj': page_obj,
        'orders': orders,
        'departments': departments,
        'formset': formset,
    }

    return render(request, 'orders/department_orders_list.html', context)


# Добавить заявку
@login_required
def order_add(request):
    if request.method == 'POST':
        formset = OrderAddFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()
            for form in formset.deleted_objects:
                form.delete()

            dt_now = datetime.datetime.now()
            year, month, day = dt_now.year, dt_now.month, dt_now.day

            return redirect(
                'orders:orders_list', year, month, day
            )

    formset = OrderAddFormSet(queryset=Order.objects.none())

    return render(
        request, 'orders/order_add.html', {'formset': formset}
    )


# Просмотр отдельной заявки (сделать возможность редактирования
# с фиксацией даты редактирования)
@login_required
def order_detail(request):
    # Зачем и чем наполнять ? Единая заявка на несколько машин ?
    # можно добавить время подачи заявки + объединенная большая заявка если была общая
    context = {
        # 'orders': orders,
        # 'page_obj': page_obj,
    }

    return render(request, 'orders/ ..... .html', context)


# Редактирование заявки (заменить отменой заявки?)
@login_required
def order_edit(request):

    context = {
        # 'orders': orders,
        # 'page_obj': page_obj,
    }

    return render(request, 'orders/ ..... .html', context)


# Удаление заявки (отказ)
@login_required
def order_delete(request):
    # Сделать отказ по заявке

    context = {
        # 'orders': orders,
        # 'page_obj': page_obj,
    }

    return render(request, 'orders/ ..... .html', context)
