from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Car, Column, TypeCar

User = get_user_model()


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
        cls.car = Car.objects.create(
            brand='Камаз',
            reg_mark='О111ОО64',
            type=cls.type_car,
            column=cls.column,
        )

    def test_models_have_correct_title(self):
        """У моделей корректно работает __str__."""
        car = CarModelTest.car

        self.assertEqual(car.reg_mark, self.car.reg_mark)
        self.assertEqual(car.column.title, self.car.column.title)
        self.assertEqual(car.type.title, self.car.type.title)