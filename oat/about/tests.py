from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class URLPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_url_exists_for_all_users(self):
        """URL адреса доступны для всех пользователей."""
        url = (
            '/about/',
        )
        for address in url:
            with self.subTest(address=address):
                response = self.guest_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                response = self.authorized_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адресов /about/."""
        urls_templates = (
            ('/about/', 'about/info.html'),
        )

        for url, template in urls_templates:
            with self.subTest(url=url):
                response = self.guest_user.get(url)
                self.assertTemplateUsed(response, template)
