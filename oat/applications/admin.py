from django.contrib import admin

from .models import Application, Department


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'order_date',
        'car',
        'type_car',
        'route_movement',
        'time_delivery_car_on_base',
        'time_delivery_car_on_borehole',
        'quantity_hours',
        'note',
    )
    search_fields = ('order_date', 'route_movement', 'note')
    list_filter = ('route_movement',)
    empty_value_display = '-пусто-'
    list_editable = ('car',)


admin.site.register(Application, ApplicationAdmin)

admin.site.register(Department)
