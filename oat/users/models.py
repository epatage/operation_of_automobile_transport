from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Department(models.Model):
    """Удаление департамента при наличии связи с заявкой невозможно!
    Департамент может редактироваться. Департамент может быть
    активирован/деактивирован для перевода из/в архивное состояние.
    """

    title = models.CharField(
        max_length=30,
        verbose_name='Подразделение',
        help_text='Цех/отдел/департамент',
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        null=True,
    )
    active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.title


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Имя пользователя содержит недопустимый символ",
            )
        ],
    )
    patronymic = models.CharField(
        max_length=50,
        verbose_name='Отчество',
        help_text='Отчество',
    )
    position = models.CharField(
        max_length=250,
        verbose_name='Должность',
        help_text='Должность',
    )
    department = models.ForeignKey(
        'Department',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name='Подразделение',
        help_text='Цех/отдел/департамент',
    )

    def __str__(self):
        return self.last_name or ''
