from cars.models import Car, Column, TypeCar
from django.test import TestCase
from users.models import User, Department

from ..models import Order


class OrderModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = Department.objects.create(
            title='Департамент',
            slug='department-test',
        )
        cls.user = User.objects.create(
            username='',
            last_name='Иванов',
            first_name='Иван',
            patronymic='Иванович',
            department=cls.department,
            position='Специалист',
        )

        cls.column_num_1 = Column.objects.create(
            title='Автоколонна_1_test',
            location='Локация_1_test',
            slug='AK_1_test',
        )
        cls.column_num_2 = Column.objects.create(
            title='Автоколонна_2_test',
            location='Локация_2_test',
            slug='AK_2_test',
        )
        cls.type_car_truck = TypeCar.objects.create(
            title='грузовая_test',
            slug='truck_test',
        )
        cls.type_car_autocrane = TypeCar.objects.create(
            title='автокран_test',
            slug='autocrane_test',
        )
        cls.car_truck = Car.objects.create(
            brand='Камаз',
            reg_mark='В111ВО64',
            type_car=cls.type_car_truck,
            column=cls.column_num_1,
        )
        cls.car_autocrane = Car.objects.create(
            brand='Урал',
            reg_mark='В222ВО64',
            type_car=cls.type_car_autocrane,
            column=cls.column_num_2,
        )
        cls.order_1 = Order.objects.create(
            car=cls.car_truck,
            type_car=cls.type_car_truck,
            route_movement='По маршруту',
            time_delivery_car_on_base='8',
            time_delivery_car_on_borehole='10',
            quantity_hours=8,
            note='Комментарий',
            department=cls.department,
            pub_date='2023-10-27 11:10:49',
            edit_date='2023-10-28 11:10:49',
            order_date='2023-10-30',
            customer=cls.user
        )

    def test_models_have_correct_title(self):
        """У моделей корректно работает __str__."""

        order = OrderModelTest.order_1

        self.assertEqual(
            str(order),
            f'Маршрут:{self.order_1.route_movement}, Тип ТС: {self.order_1.type_car}',
            '__str__ модели Order выводит не верное значение'
        )
