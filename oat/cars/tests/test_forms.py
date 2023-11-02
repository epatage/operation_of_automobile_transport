from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Car, TypeCar, Column

User = get_user_model()


class CarAndColumnViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Вася')

        cls.column_num_1 = Column.objects.create(
            title='Автоколонна_1',
            location='Степное',
            slug='AK_1',
        )
        cls.column_num_2 = Column.objects.create(
            title='Автоколонна_2',
            location='Саратов',
            slug='AK_2',
        )
        cls.type_car_truck = TypeCar.objects.create(
            title='грузовая',
            slug='truck',
        )
        cls.type_car_autocrane = TypeCar.objects.create(
            title='автокран',
            slug='autocrane',
        )
        cls.car_truck = Car.objects.create(
            brand='Камаз',
            reg_mark='В111ВО64',
            type=cls.type_car_truck,
            column=cls.column_num_1,
        )
        cls.car_autocrane = Car.objects.create(
            brand='Урал',
            reg_mark='Р929ОВ64',
            type=cls.type_car_autocrane,
            column=cls.column_num_2,
        )

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(CarAndColumnViewTest.user)

    def test_add_car_form_create_new_car(self):
        """Валидная форма создает запись в Car."""
        car_count = Car.objects.count()

        form_data = {
            'reg_mark': 'Р000РР64',
            'brand': 'Камаз',
            'type': self.type_car_autocrane.id,
            'column': self.column_num_1.id,
        }

        response = self.authorized_user.post(
            reverse('cars:car_add'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Car.objects.count(), car_count + 1)
        self.assertTrue(
            Car.objects.filter(
                reg_mark='Р000РР64',
                brand='Камаз',
                type=self.type_car_autocrane,
                column=self.column_num_1,
            ).exists()
        )
        self.assertRedirects(response, reverse('cars:cars_list'))

    def test_car_edit_form_change_cars_info(self):
        """Валидная форма редактирует запись в Car."""
        self.car = Car.objects.create(
            reg_mark='Т000ТТ64',
            brand='ВАЗ',
            type=self.type_car_autocrane,
            column=self.column_num_1,
        )

        cars_count = Car.objects.count()

        form_data = {
            'reg_mark': 'Н111НН64',
            'brand': 'ГАЗ',
            'type': self.type_car_truck,
            'column': self.column_num_2,
        }

        self.authorized_user.post(
            reverse('cars:car_edit', kwargs={'car_id': self.car.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Car.objects.count(), cars_count)
        self.assertNotEqual(self.car.reg_mark, form_data['reg_mark'])
        self.assertNotEqual(self.car.type, form_data['type'])
        self.assertNotEqual(self.car.brand, form_data['brand'])
        self.assertNotEqual(self.car.column, form_data['column'])
