import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import DateForm, OrderAddFormSet, OrderCloseFormSet, OrderEditForm
from .models import Order, Department
# from .db_query import query_debugger


# Количество заявок на странице для пагинатора
ORDERS_ON_PAGE: int = 10


@login_required
def home_page(request):
    """
    Стартовая страница.

    Переводит пользователя на страницу заявок текущей даты.
    """

    dt_now = datetime.datetime.now()

    return redirect(
        'orders:orders_list',
        year=dt_now.year,
        month=dt_now.month,
        day=dt_now.day,
    )


def get_date():
    """Получение даты для формы даты в Заявке."""

    dt_now = datetime.datetime.now()
    year = dt_now.year
    month = dt_now.month
    day = dt_now.day

    return year, month, day


# @query_debugger
@login_required
def orders_list(request, year=None, month=None, day=None):
    """Общий список заявок на главной странице по дням."""

    # В случае отсутствия данных в форме будет открывать текущий день
    if not year or not month or not day:
        year, month, day = get_date()

    date = DateForm(
        request.GET or None,
        initial={'year': year, 'month': month, 'day': day},
        prefix='date'
    )

    if date.is_valid():
        year = date.cleaned_data['year']
        month = date.cleaned_data['month']
        day = date.cleaned_data['day']
    else:
        # Если данные некорректны будет открывать текущий день
        year, month, day = get_date()

    orders = Order.objects.filter(
        order_date__year=year, order_date__month=month, order_date__day=day
    )

    if request.method == 'POST':
        formset = OrderCloseFormSet(
            request.POST or None, queryset=orders, prefix='order'
        )
        if formset.is_valid():
            formset.save()

            return redirect('orders:orders_list', year, month, day)

    formset = OrderCloseFormSet(queryset=orders, prefix='order')

    # Список подразделений для переключений в закладках
    departments = Department.objects.all()

    context = {
        'orders': orders,
        'formset': formset,
        'year': year,
        'month': month,
        'day': day,
        'date': date,
        'departments': departments,
    }

    return render(request, 'orders/orders_list.html', context)


def paginator(request, queryset):
    """Функция разделения (пагинации) заявок по страницам."""

    paginator = Paginator(queryset, ORDERS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {'page_obj': page_obj}


@login_required
def department_orders_list(request, slug):
    """
    Список заявок по подразделениям-заказчикам.

    Отдаются все существующие заявки подразделения в порядке убывания по дате
    публикации. Список разбит на страницы.
    """

    department = get_object_or_404(Department, slug=slug)
    orders = department.orders.all()

    # Список подразделений для переключения в закладках
    departments = Department.objects.all()

    # Использование функции пагинации списка заявок
    page_obj = paginator(request, orders)

    context = {
        'orders': orders,
        'departments': departments,
    }

    context.update(page_obj)

    return render(request, 'orders/department_orders_list.html', context)


@login_required
def order_add(request):
    """Добавить заявку."""

    if request.method == 'POST':
        formset = OrderAddFormSet(request.POST or None)
        if formset.is_valid():
            orders = formset.save(commit=False)
            for order in orders:
                order.customer = request.user
                order.department = request.user.department
                order.save()

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


@login_required
def order_detail(request, order_id):
    """
    Подробная информация по заявке.

    Для ознакомления с полной информацией по заявке. Помимо основных данных,
    присутствует информация по сотруднику отправившему заявку, дате и времени
    публикации заявки.
    Представитель структурного подразделения, являющегося заказчиком
    по данной заявке, может производить редактирование заявки.
    При проведении редактирования заявки заполняется поле
    "Дата и время редактирования заявки".
    """

    text = 'text'

    order = get_object_or_404(Order, id=order_id)
    user = request.user

    context = {
        'order': order,
        'id': order_id,  # Убрать !
        'text': text,  # Убрать !
        'user': user,  # Убрать ?
    }

    return render(request, 'orders/order_detail.html', context)


# Редактирование заявки (заменить отменой заявки?)
@login_required
def order_edit(request, order_id):
    """
    Редактирование заявки.

    Изменение данных заявки может делать только пользователь относящийся к
    подразделению-заказчику.
    При сохранении отредактированных данных обновляется информация по дате и
    времени последнего изменения заявки.
    """

    order = get_object_or_404(Order, id=order_id)

    if order.department != request.user.department:
        return redirect('orders:order_detail', order_id=order.id)

    form = OrderEditForm(
        request.POST or None,
        instance=order,
    )
    context = {'form': form, 'is_edit': True}

    if form.is_valid():
        form.save()
        return redirect('orders:order_detail', order_id=order_id)
    return render(request, 'orders/order_add.html', context)


# Удаление заявки (отказ)
@login_required
def order_delete(request):
    # Сделать отказ по заявке

    context = {
        # 'orders': orders,
        # 'page_obj': page_obj,
    }

    return render(request, 'orders/ ..... .html', context)
