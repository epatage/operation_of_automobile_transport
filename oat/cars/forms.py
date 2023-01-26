from django import forms
from .models import Car


class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'reg_mark', 'type', 'column')
        labels = {'brand': 'Марка', 'reg_mark': 'ГРЗ', 'type': 'Тип ТС', 'column': 'Автоколонна'}
