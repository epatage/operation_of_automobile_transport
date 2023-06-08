from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Application, Department
from cars.models import TypeCar, Car
from .forms import DateForm, ApplicationAddForm, ApplicationEditForm, ApplicationAddFormSet, ApplicationCloseForm, ApplicationCloseFormSet
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
def applications_list_(request):
    applications = Application.objects.all()

    departments = Department.objects.all()
    cars = Car.objects.all()

    if request.method == 'POST':
        formset = ApplicationCloseFormSet(request.POST, queryset=applications)
        if formset.is_valid():
            # for form in formset:
            #     form.save()
            # formset = formset.save(commit=False)  # возврат несохраненных полей
            formset.save()

    formset = ApplicationCloseFormSet(queryset=applications)
    context = {
        'applications': applications,
        'formset': formset,
        'is_edit': True,
        'departments': departments,
    }

    return render(request, 'applications/applications_list.html', context)



# Общий список заявок на главной странице (по дням)
@login_required
def applications_list(request, year, month, day):
    # date = datetime.date(int(year), int(month), int(day))
    # show_date = date.strftime("%Y-%m-%d")
    # print(show_date, 'show_date')

    # dt_now = datetime.datetime.now()
    # print(dt_now)

    departments = Department.objects.all()

    date = DateForm(request.GET or None, initial={'year': year, 'month': month, 'day': day})

    if request.method == 'GET':
        if date.is_valid():
            year = date.cleaned_data['year']
            month = date.cleaned_data['month']
            day = date.cleaned_data['day']
        applications = Application.objects.filter(order_date__year=year, order_date__month=month, order_date__day=day)

        formset = ApplicationCloseFormSet(queryset=applications)
        context = {
            'applications': applications,
            'formset': formset,
            'departments': departments,
            'year': year,
            'month': month,
            'day': day,
            'date': date,
        }

        return render(request, 'applications/applications_list.html', context)

    applications = Application.objects.filter(order_date__year=year, order_date__month=month, order_date__day=day)

    if request.method == 'POST':
        formset = ApplicationCloseFormSet(request.POST, queryset=applications)
        if formset.is_valid():
            # for form in formset:
            #     form.save()
            # formset = formset.save(commit=False)  # возврат несохраненных полей
            formset.save()

    formset = ApplicationCloseFormSet(queryset=applications)
    context = {
        'applications': applications,
        'day': day,
        'month': month,
        'year': year,
        'formset': formset,
        'is_edit': True,
        'departments': departments,
        'date': date,
    }

    return render(request, 'applications/applications_list.html', context)

# Список заявок по цеховым подразделениям
@login_required
def department_applications_list(request, slug):
    department = get_object_or_404(Department, slug=slug)
    applications = department.applications.all()

    departments = Department.objects.all()

    formset = ApplicationCloseFormSet(queryset=applications)

    context = {
        # 'page_obj': page_obj,
        'applications': applications,
        'departments': departments,
        'formset': formset,
    }

    return render(request, 'applications/department_applications_list.html', context)


# Добавить заявку
@login_required
def application_add(request):
    if request.method == 'POST':
        formset = ApplicationAddFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()
            for form in formset.deleted_objects:
                form.delete()

            dt_now = datetime.datetime.now()
            year, month, day = dt_now.year, dt_now.month, dt_now.day

            return redirect(
                'applications:applications_list', year, month, day
            )

    formset = ApplicationAddFormSet(queryset=Application.objects.none())

    return render(
        request, 'applications/application_add.html', {'formset': formset}
    )


# Просмотр отдельной заявки (убрать?)
@login_required
def application_detail(request):
    # Зачем и чем наполнять ? Единая заявка на несколько машин ?
    # можно добавить время подачи заявки + объединенная большая заявка если была общая
    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)


# Редактирование заявки (заменить отменой заявки?)
@login_required
def application_edit(request):
    # Зачем ?

    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)


# Удаление заявки (отказ)
@login_required
def application_delete(request):
    # Сделать отказ по заявке

    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)

