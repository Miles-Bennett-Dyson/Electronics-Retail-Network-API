from django.core.management.base import BaseCommand

from employees.models import Employee


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **options):
        try:
            employee = Employee.objects.create(
                email='super@user.com',
                is_staff=True,
                is_active=True,
                is_superuser=True,
                hire_date = "2021-01-01")
            employee.set_password('admin')
            employee.save()
            self.stdout.write('Супер-пользователь создан. \n email = super@user.com \n password =  admin ')
        except Exception as e:
            self.stdout.write(f'Ошибка создания супер-пользователя: {e}')
