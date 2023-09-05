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

    def __str__(self):
        return self.title


class User(AbstractUser):
    """Кастомная модель пользователя."""
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
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='Подразделение',
        help_text='Цех/отдел/департамент',
    )

    def __str__(self):
        return self.username
