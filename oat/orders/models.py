from django.db import models

from cars.models import TypeCar, Car
from users.models import User, Department


class Order(models.Model):
    """
    Заявка на транспортную единицу.

    Заявка связывает тип ТС, ТС, департамент, которые не могут быть удалены
    при наличии связи. Обязательные поля всегда должны оставаться заполненными.
    Каскадное удаление связанных моделей недопустимо.
    """

    car = models.ForeignKey(
        Car,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='ТС',
        help_text='Транспортное средство',
    )
    type_car = models.ForeignKey(
        TypeCar,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Тип ТС',
        help_text='Тип транспортного средства',
    )
    route_movement = models.CharField(
        'Маршрут движения',
        max_length=100,
        help_text='Маршрут движения',
    )
    time_delivery_car_on_base = models.CharField(
        'Время подачи на БПО',
        max_length=100,
        help_text='Время подачи на БПО',
        null=True,
        blank=True,
    )
    time_delivery_car_on_borehole = models.CharField(
        'Время подачи на скважину',
        max_length=100,
        help_text='Время подачи на скважину',
        null=True,
        blank=True,
    )
    quantity_hours = models.IntegerField(
        'Количество часов',
        help_text='Количество часов',
        null=True,
        blank=True,
    )
    note = models.CharField(
        'Примечание',
        max_length=300,
        help_text='Примечание',
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        Department,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Цех/отдел/департамент',
        help_text='Цех/отдел/департамент',
    )
    pub_date = models.DateTimeField(
        'Дата и время создания заявки',
        auto_now_add=True,
        auto_now=False,
        null=True,
    )
    edit_date = models.DateTimeField(
        'Дата и время последнего редактирования заявки',
        auto_now=True,
        null=True,
    )
    order_date = models.DateField(
        'Дата заявки',
        null=True,
        blank=False,
        db_index=True,
    )
    customer = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name='Заказчик',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Маршрут:{self.route_movement}, Тип ТС: {self.type_car}'
