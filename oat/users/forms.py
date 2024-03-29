from django.contrib.auth.forms import UserCreationForm
from users.models import User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'last_name',
            'first_name',
            'patronymic',
            'username',
            'email',
            'department',
            'position'
        )
