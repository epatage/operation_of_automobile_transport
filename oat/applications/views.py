from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Application, Department
from cars.models import TypeCar, Car
from .forms import ApplicationAddForm, ApplicationEditForm, ApplicationAddFormSet, ApplicationCloseForm, ApplicationCloseFormSet
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
def applications_list(request, day):
    date = datetime.date(2023, 4, 7)

    show_date = date.strftime("%Y-%m-%d")
    print(show_date)
    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # print(showtime)
    days = range(1, 32)

    applications = Application.objects.filter(pub_date=day) #__year=2023, pub_date__month=4, pub_date__day=day)

    departments = Department.objects.all()
    cars = Car.objects.all()

    # date = datetime.date(*time.strptime('%s-%s' % ('2023', 'апрель'), '%Y-%b')[:3])

    dates = Application.objects.all()[3]
    # print(dates.pub_date)

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
        'days': days,
        'dates': dates,
        'formset': formset,
        'is_edit': True,
        'departments': departments,
        'show_date': show_date,
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

            return redirect('applications:applications_list')

    else:
        formset = ApplicationAddFormSet(queryset=Application.objects.none())

    context = {'formset': formset}

    return render(request, 'applications/application_add.html', context)


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

