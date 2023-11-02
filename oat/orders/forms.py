from django import forms
from django.forms import modelformset_factory
from .models import Order
from .validators import validate_day, validate_year, validate_month


class BaseOrderForm(forms.ModelForm):
    """Базовая форма заявок."""

    class Meta:
        model = Order
        fields = (
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
        )


class OrderAddForm(BaseOrderForm):
    """Форма для добавления заявки."""

    class Meta(BaseOrderForm.Meta):
        exclude = ('department',)
        widgets = {
            'order_date': forms.TextInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 150px',
                'placeholder': 'Дата заявки'
            }),
            'type_car': forms.Select(attrs={
                'class': 'form-control-sm',
                'style': 'width: 100px',
                'placeholder': 'Тип ТС'
            }),
            'route_movement': forms.TextInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 240px',
                'placeholder': 'Маршрут движения'
            }),
            'time_delivery_car_on_base': forms.TextInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 170px',
                'placeholder': 'Время подачи на БПО',
            }),
            'time_delivery_car_on_borehole': forms.TextInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 170px',
                'placeholder': 'Время подачи на скв.',
            }),
            'quantity_hours': forms.NumberInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 120px',
                'placeholder': 'Кол-во часов',
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control-sm',
                'style': 'width: 200px',
                'placeholder': 'Примечание',
            }),
        }


class OrderEditForm(BaseOrderForm):
    """Форма для редактирования заявки."""

    class Meta(BaseOrderForm.Meta):
        exclude = ('department',)


class OrderCloseForm(BaseOrderForm):
    """Форма для закрытия заявок на главной странице."""

    class Meta(BaseOrderForm.Meta):
        model = Order
        fields = ('car',) + BaseOrderForm.Meta.fields

        widgets = {
            'car': forms.Select(attrs={'style': 'width: 100%'}),
            'type_car': forms.Select(attrs={'style': 'width: 100%'}),
            'route_movement': forms.TextInput(
                attrs={'readonly': 'True', 'style': 'width: 100%'}
            ),
            'time_delivery_car_on_base': forms.TextInput(
                attrs={'readonly': 'True', 'style': 'width: 100%'}
            ),
            'time_delivery_car_on_borehole': forms.TextInput(
                attrs={'readonly': 'True', 'style': 'width: 100%'}
            ),
            'quantity_hours': forms.TextInput(
                attrs={'readonly': 'True', 'style': 'width: 100%'}
            ),
            'note': forms.TextInput(
                attrs={'readonly': 'True', 'style': 'width: 100%'}
            ),
            'department': forms.Select(attrs={'style': 'width: 100%'}),
        }


"""FormSet для оформления (подачи) заявки."""
OrderAddFormSet = modelformset_factory(
    Order,
    form=OrderAddForm,
    extra=1,
    can_delete=False,
)


"""FormSet для вывода заявок на главную страницу (закрытие заявок)."""
OrderCloseFormSet = modelformset_factory(
    Order,
    form=OrderCloseForm,
    extra=0,
    can_delete=False,
)


class DateForm(forms.Form):
    """Форма выбора даты."""

    year = forms.IntegerField(
        label='Год',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm',
            'style': 'width: 200px',
        }),
        validators=[validate_year]
    )
    month = forms.IntegerField(
        label='Месяц',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm',
            'style': 'width: 200px',
        }),
        validators=[validate_month]
    )
    day = forms.IntegerField(
        label='День',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm',
            'style': 'width: 200px',
        }),
        validators=[validate_day]
    )
