from django.contrib import admin

from .models import Application, Department


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'reg_mark',
        'type_car',
        'route_movement',
        'time_delivery_car_on_base',
        'time_delivery_car_on_borehole',
        'quantity_hours',
        'note',
    )
    search_fields = ('route_movement', 'note')
    list_filter = ('route_movement',)
    empty_value_display = '-пусто-'
    list_editable = ('reg_mark',)


admin.site.register(Application, ApplicationAdmin)

admin.site.register(Department)
