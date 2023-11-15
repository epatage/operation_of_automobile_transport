from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Department

from ..models import Car, TypeCar, Column


class CarFormTest(TestCase):
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

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(CarFormTest.user)

    def test_add_car_form_create_new_car(self):
        """Валидная форма создает запись в Car."""

        car_count = Car.objects.count()

        form_data = {
            'reg_mark': 'Р000РР64',
            'brand': 'Камаз',
            'type_car': self.type_car_autocrane.id,
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
                type_car=self.type_car_autocrane,
                column=self.column_num_1,
            ).exists()
        )
        self.assertRedirects(response, reverse('cars:cars_list'))

    def test_car_edit_form_change_cars_info(self):
        """Валидная форма редактирует запись в Car."""
        self.car = Car.objects.create(
            reg_mark='Т000ТТ64',
            brand='ВАЗ',
            type_car=self.type_car_autocrane,
            column=self.column_num_1,
        )

        cars_count = Car.objects.count()

        form_data = {
            'reg_mark': 'Н111НН64',
            'brand': 'ГАЗ',
            'type_car': self.type_car_truck,
            'column': self.column_num_2,
        }

        self.authorized_user.post(
            reverse('cars:car_edit', kwargs={'car_id': self.car.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Car.objects.count(), cars_count)
        self.assertNotEqual(self.car.reg_mark, form_data['reg_mark'])
        self.assertNotEqual(self.car.type_car, form_data['type_car'])
        self.assertNotEqual(self.car.brand, form_data['brand'])
        self.assertNotEqual(self.car.column, form_data['column'])
