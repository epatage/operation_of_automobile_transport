from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
#from .models import MODEL


# Общий список заявок на главной странице
@login_required
def applications_list(request):
    applications = Application.objects.all()

    ##################### paginator
    applications = Application.objects.all().order_by('-pub_date')  # Порядок определить в МЕТА
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



    context = {
        'applications': applications,
        'page_obj': page_obj,
    }

    return render(request, 'applications/applications_list.html', context)

