from django.contrib import admin

from .models import User, Department


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'patronymic',
        'department',
        'position',
        'email',
    )
    search_fields = ('username',)
    list_filter = ('email', 'last_name', 'department')
    empty_value_display = '-пусто-'


admin.site.register(Department)
