from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .forms import CreationForm
from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('cars:cars_list')
    template_name = 'users/signup.html'


# Информация по пользователю
def profile(request, username):
    user = get_object_or_404(User, username=username)
    # user_info = user.info.get(user.id)

    context = {
        # context
    }
    return render(request, 'users/profile.html', context)  # Шаблон надо править !!
