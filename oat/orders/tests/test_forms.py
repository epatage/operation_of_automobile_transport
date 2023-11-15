from cars.models import Car, TypeCar, Column
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Department

from ..models import Order


class OrderFormTest(TestCase):
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
            order_date='2023-10-30',
            customer=cls.user
        )
        cls.order_2 = Order.objects.create(
            car=cls.car_autocrane,
            type_car=cls.type_car_autocrane,
            route_movement='По маршруту',
            time_delivery_car_on_base='8',
            time_delivery_car_on_borehole='10',
            quantity_hours=8,
            note='Комментарий',
            department=cls.department,
            order_date='2023-10-30',
            customer=cls.user
        )

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(OrderFormTest.user)

    def test_order_edit_form_change_cars_info(self):
        """Валидная форма редактирует запись в Order."""

        self.order_3 = Order.objects.create(
            car=self.car_autocrane,
            type_car=self.type_car_autocrane,
            route_movement='Тестовый маршрут',
            time_delivery_car_on_base='8',
            time_delivery_car_on_borehole='10',
            quantity_hours=8,
            note='Комментарий',
            department=self.department,
            order_date='2023-10-30',
            customer=self.user
        )

        orders_count = Order.objects.count()

        form_data = {
            'car': self.car_truck,
            'type_car': self.type_car_truck,
            'route_movement': 'Измененный маршрут',
        }

        self.authorized_user.post(
            reverse('orders:order_edit', kwargs={'order_id': self.order_3.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Order.objects.count(), orders_count)
        self.assertNotEqual(self.order_3.car, form_data['car'])
        self.assertNotEqual(self.order_3.type_car, form_data['type_car'])
        self.assertNotEqual(
            self.order_3.route_movement,
            form_data['route_movement'],
        )
