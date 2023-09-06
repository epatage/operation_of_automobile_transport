from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .forms import CreationForm
from .models import User
from django.contrib.auth.decorators import login_required


class SignUp(CreateView):
    """Авторизация пользователя."""
    form_class = CreationForm
    success_url = reverse_lazy('cars:cars_list')
    template_name = 'users/signup.html'


@login_required()
def users_list(request):
    """Список сотрудников."""
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'users/users_list.html', context)


@login_required()
def profile(request, username):
    """Профайл пользователя."""
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)
