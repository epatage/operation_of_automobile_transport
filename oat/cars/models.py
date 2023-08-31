from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=50)
    reg_mark = models.CharField(max_length=10)
    type = models.ForeignKey(
        'TypeCar',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='cars',
        verbose_name='Тип',
        help_text='Тип транспортного средства',
        default='=тип не указан=',
    )
    column = models.ForeignKey(
        'Column',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='cars',
        verbose_name='Колонна',
        help_text='Автотранспортная колонна',
        default='=колонна не указана=',
    )
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.reg_mark}'


class Column(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    slug = models.SlugField('slug', unique=True)

    def __str__(self):
        return self.title


class TypeCar(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField('slug', unique=True)
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.title
