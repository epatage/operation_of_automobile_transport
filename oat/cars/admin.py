from django.contrib import admin

from .models import Car, Column, TypeCar


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'type_car', 'reg_mark', 'column', 'active')
    search_fields = ('brand', 'type_car', 'reg_mark')
    list_filter = ('type_car', 'column')
    empty_value_display = '- не назначено -'
    list_editable = ('column', 'type_car', 'active')


admin.site.register(Car, CarAdmin)

admin.site.register(Column)

admin.site.register(TypeCar)
