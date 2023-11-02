from django.test import TestCase, Client
from ..models import Car, TypeCar, Column
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class CarURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Вася')

        cls.column = Column.objects.create(
            title='Автоколонна',
            location='Саратов',
            slug='AK',
        )
        cls.type_car = TypeCar.objects.create(
            title='грузовая',
            slug='truck',
        )
        cls.car = Car.objects.create(
            brand='Камаз',
            reg_mark='О111ОО64',
            type=cls.type_car,
            column=cls.column,
        )

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(CarURLTest.user)

    def test_urls_exists_authorized_user(self):
        """URL адреса доступны для авторизированных пользователей."""
        url = (
            '/cars/',
            f'/cars/column/{self.column.slug}/',
            f'/cars/{self.car.id}/',
            '/cars/add/',
            f'/cars/{self.car.id}/edit/',
            f'/cars/{self.car.id}/delete/',
        )

        for address in url:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                response = self.guest_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_redirect_unauthorized_user(self):
        """URL адреса не доступны (редирект) для анонимных пользователей."""
        url = (
            '/cars/',
            f'/cars/column/{self.column.slug}/',
            f'/cars/{self.car.id}/',
            '/cars/add/',
            f'/cars/{self.car.id}/edit/',
            f'/cars/{self.car.id}/delete/',
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
            ('/cars/', 'cars/cars_list.html'),
            (
                f'/cars/column/{self.column.slug}/',
                'cars/column_cars_list.html',
            ),
            (f'/cars/{self.car.id}/', 'cars/car_detail.html'),
            ('/cars/add/', 'cars/car_add.html'),
            (f'/cars/{self.car.id}/edit/', 'cars/car_add.html'),
            ('/cars/nonexistent/', 'core/404.html'),  # Не существующая стр.
        )
        for address, template in url_templates_names:
            with self.subTest(address=address):
                response = self.authorized_user.get(address)
                self.assertTemplateUsed(response, template)
