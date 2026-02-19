from django.core.management.base import BaseCommand

from employees.models import Employee


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **options):
        try:
            employee = Employee.objects.create(email='super@user.com')
            employee.is_staff = True
            employee.is_active = True
            employee.is_superuser = True
            employee.set_password('admin')
            employee.save()
            self.stdout.write(self.style.SUCCESS('Супер-пользователь создан. \n email = super@user.com \n password =  admin '))
        except Exception as e:
            self.stdout.write(
                self.style.DANGER(f'Ошибка создания супер-пользователя: {e}'))
