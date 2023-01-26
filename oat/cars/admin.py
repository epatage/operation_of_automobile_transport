from django.contrib import admin

from .models import Car, Column, TypeCar


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'type', 'reg_mark', 'column')
    search_fields = ('brand', 'type', 'reg_mark')
    list_filter = ('type',)
    empty_value_display = '-пусто-'
    list_editable = ('column', 'type')


admin.site.register(Car, CarAdmin)

admin.site.register(Column)

admin.site.register(TypeCar)
