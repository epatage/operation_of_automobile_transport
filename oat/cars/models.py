from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    reg_mark = models.CharField(max_length=10)
    column = models.ForeignKey(
        'Column',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='cars',
    )

    def __str__(self):
        return self.reg_mark


class Column(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    slug = models.SlugField('slug', unique=True)

    def __str__(self):
        return self.title
