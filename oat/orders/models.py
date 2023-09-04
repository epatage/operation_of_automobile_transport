from django.db import models

from cars.models import TypeCar, Car
from users.models import User, Department


class Order(models.Model):
    """Заявка связывает тип ТС, ТС, департамент, которые не могут быть удалены
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
        Department,
        blank=True,  # Менять на False
        null=True,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Цех/отдел/департамент',
        help_text='Цех/отдел/департамент',
    )
    pub_date = models.DateTimeField(
        'Дата подачи заявки',
        auto_now_add=True,
        null=True,
        blank=False,
    )
    order_date = models.DateField(
        'Дата заявки',
        null=True,
        blank=False,
        help_text='Укажите дату на которую заявляется транспорт',
    )

    """
    Заказчика нужно вынести в отдельную модель с ФИО, должностью, отделом.
    В раздел отдела будет передаваться информация с пользователя подающего
    заявку. Сделать связь многие-ко-многим.
    """
    customer = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.PROTECT,
        null=True,
        blank=True,  # Менять на False
        verbose_name='Заказчик',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.route_movement} {self.type_car}'


