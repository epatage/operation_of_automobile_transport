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
        formset = ApplicationCloseFormSet(request.POST or None, queryset=applications)
        for form in formset:
            print(form)
        if formset.is_valid():

            for form in formset:
                print('valid')
                form.save()
            # formset = formset.save(commit=False)  # возврат несохраненных полей
            # formset.save()

            return render(request, 'applications/applications_list.html', {'formset': formset})
    print('no valid')
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
    # form = ApplicationAddForm(request.POST or None)
    # ApplicationAddFormSet = modelformset_factory(Application, exclude=())  # fields='__all__')

    if request.method == 'POST':
        formset = ApplicationAddFormSet(request.POST or None)
        if formset.is_valid():
            formset.save()

    else:
        formset = ApplicationAddFormSet(queryset=Application.objects.none())


    # form = ApplicationAddForm(request.POST or None)
    # if form.is_valid():
    #     application = form.save(commit=False)
    #     application.save()

    context = {
        # 'form': form,
        'formset': formset
        # 'page_obj': page_obj,
    }

    return render(request, 'applications/application_add.html', context)



#
# # Добавить заявку formset через класс
# class ApplicationAddView(CreateView):
#     form_class = ApplicationAddFormSet
#     model = Application
#     template_name = 'applications/application_add.html'
#     # Переадресация пользователя после успешной отправки заявки
#     success_url = reverse_lazy('applications:department')
#
#
#     # # Здесь нужно настроить валидацию формы
#     #
#     # def application_form_valid(self, form):
#     #     named_formsets = self.get_named_formsets()
#     #     if not all((field.is_valid() for field in named_formsets.values())):
#     #         return self.render_to_response(self.get_context_data(form=form))
#     #
#     #     self.object = form.save()
#     #
#     #     # for every formset, attempt to find a specific formset save function
#     #     # otherwise, just save.
#     #     for name, formset in named_formsets.items():
#     #         formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
#     #         if formset_save_func is not None:
#     #             formset_save_func(formset)
#     #         else:
#     #             formset.save()
#     #     return redirect('products:list_products')
#
#
#     def application_form(self, formset):
#
#         applications = formset.save(commit=False)  # self.save_formset(formset, contact)
#         # add this 2 lines, if you have can_delete=True parameter
#         # set in inlineformset_factory func
#         for obj in formset.deleted_objects:
#             obj.delete()
#         for application in applications:
#             application.save()
#
#     def get_context_data(self):
#         ctx = super()
#         ctx['named_formsets'] = self.get_named_formsets()
#         return ctx
#
#     def get_named_formsets(self):
#         return {
#             'applications': ApplicationAddFormSet(self.request.POST or None, instance=self.object,
#                                        prefix='applications'),
#             }
#         form = ApplicationAddForm(request.POST or None)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.save()
#
#         context = {
#             'form': formset,
#
#             # 'page_obj': page_obj,
#         }
#
#         return render(request, 'applications/application_add.html', context)
#
#


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

