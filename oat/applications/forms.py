from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Application
from cars.models import Car


class ApplicationAddForm(forms.ModelForm):
    """Форма для добавления заявки."""
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
        widgets = {
            'reg_mark': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'brand': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'type_car': forms.Select(attrs={'class': 'form-control-sm'}),
            'route_movement': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'time_delivery_car_on_base': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'time_delivery_car_on_borehole': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'quantity_hours': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'note': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'department': forms.TextInput(attrs={'class': 'form-control-sm'}),
        }
        lables = {
            'reg_mark': 'Номерной знак'
        }


# Нужно изменить поля формы
# не все поля можно менять, добавляется поле "время изменения заявки"
class ApplicationEditForm(forms.ModelForm):
    """Форма для редактирования заявки."""
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
        widgets = {
            'size': forms.TextInput(            # size ??
                attrs={
                    'class': 'form-control',
                }
            ),
        }


"""FormSet для оформления (подачи) заявки."""
ApplicationAddFormSet = modelformset_factory(
    Application,
    form=ApplicationAddForm,
    extra=1,
    can_delete=True,
)


# Нужно изменить поля формы
# не все поля можно менять, добавляется поле "время изменения заявки"
class ApplicationCloseForm(forms.ModelForm):
    """Форма для закрытия заявок на главной странице."""
    class Meta:
        model = Application
        fields = (
            'reg_mark',
            'brand',
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            # 'department',
        )

        widgets = {
            'reg_mark': forms.Select(attrs={'style': 'width: 100px'}),
            'brand': forms.Select(attrs={'style': 'width: 130px'}),
            'type_car': forms.Select(attrs={ 'style': 'width: 100px'}),
            'route_movement': forms.TextInput(attrs={ 'style': 'width: 200px'}),
            'time_delivery_car_on_base': forms.TextInput(attrs={'disabled': 'True', 'style': 'width: 80px'}),
            'time_delivery_car_on_borehole': forms.TextInput(attrs={'disabled': 'True', 'style': 'width: 80px'}),
            'quantity_hours': forms.TextInput(attrs={'disabled': 'True', 'style': 'width: 80px'}),
            'note': forms.TextInput(attrs={'disabled': 'True', 'style': 'width: 150px'}),
            'department': forms.TextInput(attrs={'disabled': 'True', 'style': 'width: 80px'}),
        }


"""FormSet для вывода заявок на главную страницу (закрытие заявок)."""
ApplicationCloseFormSet = modelformset_factory(
    Application,
    form=ApplicationCloseForm,
    extra=0,
    can_delete=False,
)
