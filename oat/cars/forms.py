from django import forms
from .models import Car


class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'reg_mark', 'type_car', 'column')
        labels = {
            'brand': 'Марка',
            'reg_mark': 'ГРЗ',
            'type_car': 'Тип ТС',
            'column': 'Автоколонна',
        }


class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'reg_mark', 'type_car', 'column')
        labels = {
            'brand': 'Марка',
            'reg_mark': 'ГРЗ',
            'type_car': 'Тип ТС',
            'column': 'Автоколонна',
        }
