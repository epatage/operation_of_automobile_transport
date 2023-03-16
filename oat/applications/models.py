from django.db import models
from django.contrib.auth import get_user_model

from cars.models import TypeCar, Car

User = get_user_model()


class Application(models.Model):
    reg_mark = models.ForeignKey(
        Car,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='cars_mark',
        verbose_name='ГРЗ',
        help_text='Гос.рег.знак',
    )
    brand = models.ForeignKey(
        Car,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='cars_brand',
        verbose_name='Марка ТС',
        help_text='Марка транспортного средства',
    )
    type_car = models.ForeignKey(
        TypeCar,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='types',
        verbose_name='Тип ТС',
        help_text='Тип транспортного средства',
    )
    route_movement = models.CharField(
        max_length=100,
        verbose_name='Маршрут движения',
        help_text='Маршрут движения',
    )
    time_delivery_car_on_base = models.CharField(
        max_length=100,
        verbose_name='Время подачи на БПО',
        help_text='Время подачи на БПО',
        null=True,
        blank=True,
    )
    time_delivery_car_on_borehole = models.CharField(
        max_length=100,
        verbose_name='Время подачи на скважину',
        help_text='Время подачи на скважину',
        null=True,
        blank=True,
    )
    quantity_hours = models.IntegerField(
        verbose_name='Количество часов',
        help_text='Количество часов',
        null=True,
        blank=True,
    )
    note = models.CharField(
        max_length=300,
        verbose_name='Примечание',
        help_text='Примечание',
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        'Department',
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Цех/отдел',
        help_text='Цех/отдел',
    )
    pub_date = models.DateTimeField(
        'Дата подачи заявки',
        auto_now_add=True,
        null=True,
        blank=False,
    )

    """
    Заказчика нужно вынести в отдельную модель с ФИО, должностью, отделом.
    В раздел отдела будет передаваться информация с пользователя подающего
    заявку. Сделать связь многие-ко-многим.
    """
    customer = models.ForeignKey(
        User,
        related_name='applications',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Заказчик',
    )

    def __str__(self):
        return f'{self.department} {self.route_movement} {self.type_car}'


class Department(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='Подразделение',
        help_text='Цех/отдел',
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        null=True,
    )

    def __str__(self):
        return self.title
