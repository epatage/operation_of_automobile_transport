# Generated by Django 3.2.16 on 2023-06-08 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_application_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='order_date',
            field=models.DateField(help_text='Укажите дату на которую заявляется транспорт', null=True, verbose_name='Дата заявки'),
        ),
    ]
