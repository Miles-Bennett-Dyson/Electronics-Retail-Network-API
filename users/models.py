from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """ Модель для хранения учетных записей всех пользователей. """

    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Учетная запись"
        verbose_name_plural = "Учетные записи"
        ordering = ["pk"]
