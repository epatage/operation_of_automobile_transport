from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_date',
        'car',
        'type_car',
        'route_movement',
        'time_delivery_car_on_base',
        'time_delivery_car_on_borehole',
        'quantity_hours',
        'note',
        'customer',
        'department',
        'pub_date',
    )
    search_fields = ('order_date', 'route_movement', 'note')
    list_filter = ('route_movement',)
    empty_value_display = '-пусто-'
    list_editable = ('car',)
