# Generated by Django 3.2.16 on 2023-02-15 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20230213_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
    ]