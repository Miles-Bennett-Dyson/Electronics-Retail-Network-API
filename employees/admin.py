from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'email',
        'position',
        'phone_number',
        'department',
        'hire_date'
    )
    ordering = ['hire_date']
    add_fieldsets = (
        (
            None,
            {'classes':
                 ('wide',),
             'fields':
                 (
                     'email',
                     'password',
                     'first_name',
                     'last_name',
                     'position',
                     'department',
                     'phone_number',
                     'photo',
                     'hire_date'
                 )
             }
        ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Служебная информация', {
            'fields': ('position', 'department', 'phone_number', 'photo', 'hire_date')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('last_login', 'date_joined',)
