from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Employee(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    position = models.CharField(max_length=150, verbose_name="Должность")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", **NULLABLE)
    photo = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Фотография сотрудника",
        **NULLABLE
    )
    department = models.CharField(max_length=150, verbose_name="Отдел/Подразделение")
    hire_date = models.DateField(verbose_name="Дата найма")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Сотрудник: {self.email} ({self.position})"

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"
        ordering = ["pk"]
