from django.db import models
from config import settings

NULLABLE = {"null": True, "blank": True}


class Employee(models.Model):
    """  Модель работника компании. """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name="Сотрудник"
    )
    position = models.CharField(max_length=150, verbose_name="Должность")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", **NULLABLE)
    photo = models.ImageField(upload_to="users/avatars/",verbose_name="Фотография сотрудника",**NULLABLE)
    department = models.CharField(max_length=150, verbose_name="Отдел/Подразделение")
    hire_date = models.DateField(auto_now_add=True, verbose_name="Дата найма")

    def __str__(self):
        return f"Сотрудник: {self.user.email} ({self.position})"

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"
