from django.test import TestCase, Client
from ..models import Car, TypeCar, Column
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse

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

    def test_pages_uses_correct_template(self):
        """URL-адрес при обращении по reverse-именам
         использует соответствующий шаблон.
         """
        pages_names_templates = (
            (reverse('cars:cars_list'), 'cars/cars_list.html'),
            (reverse(
                'cars:column', kwargs={'slug': self.column_num_1.slug}
            ), 'cars/column_cars_list.html'),
            (reverse(
                'cars:car_detail', kwargs={'car_id': self.car_truck.id}
            ), 'cars/car_detail.html'),
            (reverse('cars:car_add'), 'cars/car_add.html'),
            (reverse(
                'cars:car_edit', kwargs={'car_id': self.car_truck.id}
            ), 'cars/car_add.html'),
        )

        for reverse_name, template in pages_names_templates:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_cars_list_page_show_correct_context(self):
        """Шаблон cars_list сформирован с правильным контекстом."""
        response = self.authorized_user.get(reverse('cars:cars_list'))
        car_object = response.context['cars']

        for car in car_object:
            if car.id == self.car_truck.id:
                test_car = car

                car_reg_mark = test_car.reg_mark
                car_type = test_car.type.title
                car_brand = test_car.brand
                car_column = test_car.column.title

                self.assertEqual(car_reg_mark, self.car_truck.reg_mark)
                self.assertEqual(car_type, self.car_truck.type.title)
                self.assertEqual(car_brand, self.car_truck.brand)
                self.assertEqual(car_column, self.car_truck.column.title)

    def test_column_cars_list_page_show_correct_context(self):
        """Шаблон column_cars_list сформирован с правильным контекстом."""
        response = (
            self.authorized_user.get(
                reverse(
                    'cars:column', kwargs={'slug': self.column_num_1.slug}
                )))
        column_cars_list = response.context['cars']
        for car in column_cars_list:
            with self.subTest(car=car):
                self.assertEqual(car.column.title, self.column_num_1.title)

    def test_car_detail_page_show_correct_context(self):
        """Шаблон car_detail сформирован с правильным контекстом."""
        response = (
            self.authorized_user.get(
                reverse(
                    'cars:car_detail', kwargs={
                        'car_id': self.car_truck.id
                    }
                )))

        car = response.context['car']
        self.assertEqual(car.reg_mark, self.car_truck.reg_mark)
        self.assertEqual(car.column, self.car_truck.column)
        self.assertEqual(car.type, self.car_truck.type)
        self.assertEqual(car.brand, self.car_truck.brand)

    def test_car_add_page_show_correct_context(self):
        """Шаблон car_add сформирован с правильным контекстом."""
        response = self.authorized_user.get(reverse('cars:car_add'))
        form_fields = {
            'reg_mark': forms.fields.CharField,
            'type': forms.fields.ChoiceField,
            'column': forms.fields.ChoiceField,
            'brand': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_car_edit_page_show_correct_context(self):
        """Шаблон car_edit сформирован с правильным контекстом."""
        response = self.authorized_user.get(
            reverse(
                'cars:car_edit',
                kwargs={'car_id': self.car_truck.id},
            ))

        form_fields = {
            'reg_mark': forms.fields.CharField,
            'type': forms.fields.ChoiceField,
            'column': forms.fields.ChoiceField,
            'brand': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_column_cars_list_page_show_car_post_with_additional_car(self):
        """Шаблон column_cars_list отображает ТС
         с правильной привязкой по колоннам.
         """
        response = self.authorized_user.get(
            reverse(
                'cars:column', kwargs={
                    'slug': self.car_autocrane.column.slug
                }
            ))
        cars_list = response.context['cars']
        column_number = response.context['column']
        for car in cars_list:
            self.assertEqual(car.column, self.car_autocrane.column)

        self.assertEqual(column_number, self.column_num_2)
