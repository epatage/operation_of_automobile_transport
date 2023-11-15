from http import HTTPStatus

from cars.models import Car, Column, TypeCar
from django.test import TestCase, Client
from users.models import User, Department

from ..models import Order


class OrderURLTest(TestCase):
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
        cls.year = 2023
        cls.month = 10
        cls.day = 22

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(OrderURLTest.user)

    def test_urls_exists_authorized_user(self):
        """URL адреса доступны для авторизированных пользователей."""

        url = (
            f'/orders/{self.year}/{self.month}/{self.day}/',
            f'/department/{self.department.slug}/',
            '/add/',
            f'/{self.order_1.id}/',
            f'/{self.order_1.id}/edit/',
        )

        for address in url:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_authorized_user(self):
        """
        URL адреса перенаправляют авторизированных пользователей.
        """

        url = (
            '/',
        )

        for address in url:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_redirect_unauthorized_user(self):
        """
        URL адреса не доступны для анонимных пользователей.
        Перенаправление на страницу авторизации.
        """

        url = (
            f'/orders/{self.year}/{self.month}/{self.day}/',
            f'/department/{self.department.slug}/',
            '/add/',
            f'/{self.order_1.id}/',
            f'/{self.order_1.id}/edit/',
            '/',
        )

        for address in url:
            with self.subTest(address=address):
                response = self.guest_user.get(address, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={address}')

    def test_url_not_found_all_users(self):
        """URL-адреса вернут 404 всем пользователям."""

        url = (
            '/unexisting_page/',
        )

        for address in url:
            with self.subTest(address=address):
                response = self.guest_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        url_templates_names = (
            (
                f'/orders/{self.year}/{self.month}/{self.day}/',
                'orders/orders_list.html',
            ),
            (
                f'/department/{self.department.slug}/',
                'orders/department_orders_list.html',
            ),
            ('/add/', 'orders/order_add.html'),
            (f'/{self.order_1.id}/', 'orders/order_detail.html'),
            (f'/{self.order_1.id}/edit/', 'orders/order_add.html'),
            ('/orders/nonexistent/', 'core/404.html'),
        )
        for address, template in url_templates_names:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Шаблон не соответствует маршруту',
                )
