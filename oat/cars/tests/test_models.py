from django.test import TestCase

from ..models import Car, Column, TypeCar


class CarModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.column = Column.objects.create(
            title='Автоколонна',
            location='Саратов',
            slug='AK',
        )
        cls.type_car = TypeCar.objects.create(
            title='грузовая',
            slug='truck',
        )
        cls.car_1 = Car.objects.create(
            brand='Камаз',
            reg_mark='О111ОО64',
            type_car=cls.type_car,
            column=cls.column,
        )
        cls.car_2 = Car.objects.create(
            brand='Камаз',
            reg_mark='О222ОО64',
            type_car=cls.type_car,
            column=cls.column,
        )
        cls.car_3 = Car.objects.create(
            brand='Камаз',
            reg_mark='О333ОО64',
            type_car=cls.type_car,
            column=cls.column,
            active=False,
        )

    def test_models_have_correct_title(self):
        """У моделей корректно работает метод __str__."""

        car = CarModelTest.car_1
        type_car = CarModelTest.type_car
        column = CarModelTest.column

        self.assertEqual(
            str(car),
            self.car_1.reg_mark,
            '__str__ модели Car выводит не верное значение'
        )
        self.assertEqual(
            str(column),
            self.car_1.column.title,
            '__str__ модели Column выводит не верное значение'
        )
        self.assertEqual(
            str(type_car),
            self.car_1.type_car.title,
            '__str__ модели TypeCar выводит не верное значение'
        )

    def test_models_show_only_active_car(self):
        """
        В приложении доступны только автомобили в эксплуатации (активные).
        """

        cars_all_count = Car.objects.all().count()
        cars_active_count = Car.objects.filter(active=True).count()

        self.assertNotEqual(
            cars_all_count,
            cars_active_count,
            "В список транспорта выводятся не эксплуатируемые автомобили"
        )
