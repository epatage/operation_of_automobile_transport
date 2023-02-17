from django import forms
from .models import Application


class ApplicationAddForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = {
            'reg_mark',
            'brand',
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
        }


# Нужно изменить поля формы
# не все поля можно менять, добавляется поле "время изменения заявки"
class ApplicationEditForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = {
            'reg_mark',
            'brand',
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
        }
