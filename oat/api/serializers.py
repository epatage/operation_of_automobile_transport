from rest_framework import serializers

from orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'car',
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
            'car',
            'customer',
        )


class OrderCloseSerializer(serializers.ModelSerializer):
    # Нужно переопределять поля для корректного отображения
    # reg_mark = serializers.SlugRelatedField(slug_field='reg_mark')

    class Meta:
        model = Order
        fields = (
            'id',
            'car',
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
