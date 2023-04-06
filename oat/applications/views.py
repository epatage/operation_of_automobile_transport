from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Application, Department
from cars.models import TypeCar, Car
from .forms import ApplicationAddForm, ApplicationEditForm, ApplicationAddFormSet, ApplicationCloseForm, ApplicationCloseFormSet
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.forms import modelformset_factory


# Общий список заявок на главной странице
@login_required
def applications_list(request):
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
        # 'page_obj': page_obj,
        'formset': formset,
        # 'form': form,
        'is_edit': True,
        'departments': departments,
    }

    return render(request, 'applications/applications_list.html', context)


    # if form.is_valid():
    #     form.save()



    ##################### paginator
    # applications = Application.objects.all().order_by('-pub_date')  # Порядок определить в МЕТА
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядеть так:
    # post_list = Post.objects.all()

    # Показывать по 10 записей на странице.
    # Показывать по фильру даты ????
    # paginator = Paginator(applications, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    # page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    # page_obj = paginator.get_page(page_number)
    #######################




# Список заявок по цеховым подразделениям
@login_required
def department_applications_list(request, slug):
    department = get_object_or_404(Department, slug=slug)
    applications = department.applications.all()

    departments = Department.objects.all()

    context = {
        # 'page_obj': page_obj,
        'applications': applications,
        'departments': departments,
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

