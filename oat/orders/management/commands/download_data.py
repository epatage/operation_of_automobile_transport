import openpyxl
import pandas as pd
from django.core.management.base import BaseCommand
import csv
from cars.models import TypeCar, Column, Car
from users.models import User, Department
from orders.models import Order


"""
При запуске команды с аргументом --delete-existing все существующие записи
в БД удаляться! Записи пользователей с ID в диапазоне от 0 до 4 сохранятся.
Так можно создавать своих пользователей и супер пользователей до запуска
команды без дальнейшей их потери.
"""

OBJECTS_LIST = {
    'Заявка': Order,
    'ТС': Car,
    'Тип ТС': TypeCar,
    'Автоколонна': Column,
    'Департамент': Department,
    'Пользователь': User,
}


def clear_data(self):
    """
    Функция очистки БД от имеющихся данных.

    Необходима для исключения дублирования добавляемых элементов при повторном
    запуске основной команды.
    """

    for key, value in OBJECTS_LIST.items():

        if value == User:
            value.objects.exclude(id__in=[0, 1, 2, 3, 4]).delete()
        else:
            value.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Существующие записи "{key}" были удалены.'
            )
        )


class Command(BaseCommand):
    help = "Загружает CSV данные из файла data/ingredients."

    def add_arguments(self, parser):
        """Добавляет аргумент для удаления всех имеющихся в БД данных."""

        parser.add_argument(
            "--delete-existing",
            action="store_true",
            dest="delete_existing",
            default=False,
            help="Удаляет существующие данные, записанные ранее",
        )

    def handle(self, *args, **options):

        if options["delete_existing"]:
            clear_data(self)

        book = openpyxl.open('./data_test/db.xlsx', read_only=True)

        """Загрузка Типов ТС."""
        records = []

        sheet = book.worksheets[0]
        for row in range(2, 9):
            id = int(sheet[row][0].value)
            title = sheet[row][1].value
            slug = sheet[row][2].value

            record = TypeCar(id=id, title=title, slug=slug)
            records.append(record)

        TypeCar.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Типов ТС" сохранены'
        ))

        """Загрузка Автоколонн."""
        records = []

        sheet = book.worksheets[1]
        for row in range(2, 4):
            id = int(sheet[row][0].value)
            title = sheet[row][1].value
            location = sheet[row][2].value
            slug = sheet[row][3].value

            record = Column(id=id, title=title, location=location, slug=slug)
            records.append(record)

        Column.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Автоколонн" сохранены'
        ))

        """Загрузка ТС."""
        records = []

        sheet = book.worksheets[2]
        for row in range(2, 33):
            id = int(sheet[row][0].value)
            brand = sheet[row][1].value
            reg_mark = sheet[row][2].value
            type_id = (sheet[row][3].value)
            column_id = int(sheet[row][4].value)

            record = Car(id=id, brand=brand, reg_mark=reg_mark,  column_id=column_id, type_car_id=type_id,)
            records.append(record)

        Car.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Транспортных средств" сохранены'
        ))

        """Загрузка Департаментов."""
        records = []

        sheet = book.worksheets[3]
        for row in range(2, 6):
            id = sheet[row][0].value
            title = sheet[row][1].value
            slug = sheet[row][2].value

            record = Department(id=id, title=title, slug=slug)
            records.append(record)

        Department.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Департаментов" сохранены'
        ))

        """Загрузка Пользователей"""
        records = []

        sheet = book.worksheets[4]
        for row in range(2, 8):
            id = sheet[row][0].value
            last_name = sheet[row][1].value
            first_name = sheet[row][2].value
            patronymic = sheet[row][3].value
            department_id = sheet[row][4].value
            position = sheet[row][5].value
            email = sheet[row][6].value

            record = None

            try:
                record = User(
                    id=id,
                    last_name=last_name,
                    first_name=first_name,
                    patronymic=patronymic,
                    department_id=department_id,
                    position=position,
                    email=email,
                )
            except Exception:
                pass

            records.append(record)

        User.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Пользователей" сохранены'
        ))

        """Загрузка Заявок"""

        """
        Требуется оптимизация массовой загрузки объектов.
        Возможно, проблема замедления связана с индексированием.
        """

        # records = []
        n = 0
        sheet = book.worksheets[5]
        for row in range(2, 1521):
            id = sheet[row][0].value
            car = sheet[row][1].value
            type_car = sheet[row][2].value
            route_movement = sheet[row][3].value
            time_delivery_car_on_base = sheet[row][4].value
            time_delivery_car_on_borehole = sheet[row][5].value
            quantity_hours = sheet[row][6].value
            note = sheet[row][7].value
            department = sheet[row][8].value
            pub_date = sheet[row][9].value
            order_date = sheet[row][10].value
            customer = sheet[row][11].value

            # record = Order(
            #     id=id,
            #     car_id=car,
            #     type_car_id=type_car,
            #     route_movement=route_movement,
            #     time_delivery_car_on_base=time_delivery_car_on_base,
            #     time_delivery_car_on_borehole=time_delivery_car_on_borehole,
            #     quantity_hours=quantity_hours,
            #     note=note,
            #     department_id=department,
            #     pub_date=pub_date,
            #     order_date=order_date,
            #     customer_id=customer,
            # )
            Order.objects.create(
                id=id,
                car_id=car,
                type_car_id=type_car,
                route_movement=route_movement,
                time_delivery_car_on_base=time_delivery_car_on_base,
                time_delivery_car_on_borehole=time_delivery_car_on_borehole,
                quantity_hours=quantity_hours,
                note=note,
                department_id=department,
                pub_date=pub_date,
                order_date=order_date,
                customer_id=customer,
            )
            n += 1
            print(n)
            # records.append(record)

        # Order.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(
            'Все записи "Заявки" сохранены'
        ))

        book.close()
