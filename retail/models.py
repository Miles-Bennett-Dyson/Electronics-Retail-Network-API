from django.contrib import admin
from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    """ Модель для товаров. """
    name = models.CharField(max_length=150, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Retail(models.Model):
    """ Модель звена сети. """
    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    products = models.ManyToManyField(Product, verbose_name="Продукты")

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="subsidiaries"
    )

    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    @admin.display(description='Уровень иерархии в цепочке')
    def get_level(self):
        """ Метод для вычисления уровня иерархии. """
        level = 0
        current_node = self
        while current_node.supplier:
            level += 1
            current_node = current_node.supplier
        return level

    def clean(self):
        list_suppliers = []
        current_node = self.supplier
        while current_node:
            print(current_node)
            if current_node.pk in list_suppliers or current_node.pk == self.pk:
                raise ValidationError('Циклическая иерархия')
            list_suppliers.append(current_node.pk)
            current_node = current_node.supplier
        super().clean()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
