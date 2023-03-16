from rest_framework import serializers

from applications.models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = (
            'id',
            'reg_mark',
            'brand',
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
            'pub_date',
            'customer',
        )
        read_only_fields = (
            'reg_mark',
            'brand',
            'customer',
        )


class ApplicationCloseSerializer(serializers.ModelSerializer):
    # Нужно переопределять поля для корректного отображения
    # reg_mark = serializers.SlugRelatedField(slug_field='reg_mark')

    class Meta:
        model = Application
        fields = (
            'id',
            'reg_mark',
            'brand',
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
            'pub_date',
            'customer',
        )
        read_only_fields = (
            'type_car',
            'route_movement',
            'time_delivery_car_on_base',
            'time_delivery_car_on_borehole',
            'quantity_hours',
            'note',
            'department',
            'pub_date',
            'customer',
        )
