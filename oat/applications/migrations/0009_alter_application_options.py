# Generated by Django 3.2.16 on 2023-04-06 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_auto_20230316_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ('-pub_date',)},
        ),
    ]