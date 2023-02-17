from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Application, Department
from .forms import ApplicationAddForm, ApplicationEditForm


# Общий список заявок на главной странице
@login_required
def applications_list(request):
    applications = Application.objects.all()
    # вывод в форму (только по одному?)
    app = get_object_or_404(Application, pk=1)
    form = ApplicationEditForm(request.POST or None, instance=app)

    departments = Department.objects.all()

    context = {
        'applications': applications,
        # 'page_obj': page_obj,
        'form': form,
        'is_edit': True,
        'departments': departments,
    }

    if form.is_valid():
        form.save()



    ##################### paginator
    # applications = Application.objects.all().order_by('-pub_date')  # Порядок определить в МЕТА
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядеть так:
    # post_list = Post.objects.all()

    # Показывать по 10 записей на странице.
    # Показывать по фильру даты ????
    paginator = Paginator(applications, 10)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    #######################





    return render(request, 'applications/applications_list.html', context)


# Список заявок по цеховым подразделениям
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


# Список заявок по цеховым подразделениям
def application_add(request):
    # Взять форму из добавления машин
    form = ApplicationAddForm(request.POST or None)
    if form.is_valid():
        application = form.save(commit=False)
        application.save()

    context = {
        'form': form,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/application_add.html', context)


# Просмотр отдельной заявки (убрать?)
def application_detail(request):
    # Зачем и чем наполнять ? Единая заявка на несколько машин ?
    # можно добавить время подачи заявки + объединенная большая заявка если была общая
    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)


# Редактирование заявки (заменить отменой заявки?)
def application_edit(request):
    # Зачем ?

    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)


# Удаление заявки (отказ)
def application_delete(request):
    # Сделать отказ по заявке

    context = {
        # 'applications': applications,
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/ ..... .html', context)

