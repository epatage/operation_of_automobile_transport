from cars.models import Car, TypeCar, Column
from django import forms
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Department

from ..models import Order


class CarAndColumnViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = Department.objects.create(
            title='Департамент',
            slug='depart',
        )
        cls.department_inactive = Department.objects.create(
            title='Департамент_неактивный',
            slug='inactive',
            active=False,
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
            location='Степное_test',
            slug='AK_1_test_view',
        )
        cls.column_num_2 = Column.objects.create(
            title='Автоколонна_2_test',
            location='Саратов_test',
            slug='AK_2_test_view',
        )
        cls.type_car_truck = TypeCar.objects.create(
            title='грузовая_test',
            slug='truck_test_view',
        )
        cls.type_car_autocrane = TypeCar.objects.create(
            title='автокран_test',
            slug='autocrane_test_view',
        )
        cls.car_truck = Car.objects.create(
            brand='Камаз',
            reg_mark='В111ВО64',
            type_car=cls.type_car_truck,
            column=cls.column_num_1,
        )
        cls.car_autocrane = Car.objects.create(
            brand='Урал',
            reg_mark='Р929ОВ64',
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

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(CarAndColumnViewTest.user)

    def test_pages_uses_correct_template(self):
        """
        URL-адрес при обращении по reverse-именам
        использует соответствующий шаблон.
        """

        year, month, day = self.order_1.order_date.split('-')
        pages_names_templates = (
            (reverse(
                'orders:orders_list',
                kwargs={
                    'year': year,
                    'month': month,
                    'day': day,
                }
            ), 'orders/orders_list.html'),
            (reverse(
                'orders:department_orders_list', kwargs={'slug': self.department.slug}
            ), 'orders/department_orders_list.html'),
            (reverse('orders:order_add'), 'orders/order_add.html'),
            (reverse(
                'orders:order_detail', kwargs={'order_id': self.order_1.id}
            ), 'orders/order_detail.html'),

            (reverse(
                'orders:order_edit', kwargs={'order_id': self.order_1.id}
            ), 'orders/order_add.html'),
        )

        for reverse_name, template in pages_names_templates:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_department_orders_list_page_show_correct_context(self):
        """
        Шаблон department_orders_list сформирован с правильным контекстом.
        """

        response = (
            self.authorized_user.get(
                reverse(
                    'orders:department_orders_list',
                    kwargs={'slug': self.department.slug},
                )))

        # Проверка корректности данных передающихся в таблицу заявок
        order = response.context['orders'][0]
        year, month, day = self.order_1.order_date.split('-')

        self.assertEqual(order.car, self.car_truck)
        self.assertEqual(order.type_car, self.type_car_truck)
        self.assertEqual(order.route_movement, 'По маршруту')
        self.assertEqual(order.time_delivery_car_on_base, '8')
        self.assertEqual(order.time_delivery_car_on_borehole, '10')
        self.assertEqual(order.quantity_hours, 8)
        self.assertEqual(order.note, self.order_1.note)
        self.assertEqual(order.department, self.department)
        self.assertEqual(order.pub_date, self.order_1.pub_date)
        self.assertEqual(order.edit_date, self.order_1.pub_date)
        self.assertEqual(order.order_date.year, int(year))
        self.assertEqual(order.order_date.month, int(month))
        self.assertEqual(order.order_date.day, int(day))
        self.assertEqual(order.customer, self.user)

        # Проверка передачи в контекст только "активных" подразделений
        departments = response.context['departments'].count()
        departments_list = Department.objects.all().count()

        self.assertNotEqual(
            departments,
            departments_list,
            'В список департаментов попадают неактивные подразделения',
        )

    def test_order_detail_page_show_correct_context(self):
        """Шаблон order_detail сформирован с правильным контекстом."""

        response = (
            self.authorized_user.get(
                reverse(
                    'orders:order_detail', kwargs={
                        'order_id': self.order_1.id
                    }
                )))

        order = response.context['order']
        self.assertEqual(order.car, self.car_truck)
        self.assertEqual(order.type_car, self.type_car_truck)
        self.assertEqual(order.route_movement, 'По маршруту')
        self.assertEqual(order.time_delivery_car_on_base, '8')
        self.assertEqual(order.time_delivery_car_on_borehole, '10')
        self.assertEqual(order.quantity_hours, 8)
        self.assertEqual(order.note, self.order_1.note)
        self.assertEqual(order.department, self.department)
        self.assertEqual(order.pub_date, self.order_1.pub_date)
        self.assertEqual(order.edit_date, self.order_1.pub_date)
        self.assertEqual(order.customer, self.user)

    def test_order_edit_page_show_correct_context(self):
        """Шаблон order_edit сформирован с правильным контекстом."""

        response = self.authorized_user.get(
            reverse(
                'orders:order_edit',
                kwargs={'order_id': self.order_1.id},
            ))

        form_fields = {
            'type_car': forms.fields.ChoiceField,
            'route_movement': forms.fields.CharField,
            'time_delivery_car_on_base': forms.fields.CharField,
            'time_delivery_car_on_borehole': forms.fields.CharField,
            'quantity_hours': forms.fields.IntegerField,
            'note': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

        self.assertEqual(
            response.context.get('is_edit'),
            True,
            'В контекст не передается переменная редактирования is_edit'
        )
