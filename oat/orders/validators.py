from django import forms


def validate_year(value):
    if not 2000 < value < 3000:
        raise forms.ValidationError(
            'Некорректно указан год',
            params={'value': value},
        )


def validate_month(value):
    if not 0 < value < 13:
        raise forms.ValidationError(
            'Некорректно указан месяц',
            params={'value': value},
        )


def validate_day(value):
    if not 0 < value < 32:
        raise forms.ValidationError(
            'Некорректно указан день',
            params={'value': value},
        )
