from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from retail.models import Retail, Product


class RetailCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = Employee.objects.create(
            email="test@test.com",
            first_name="Иван",
            last_name="Иванов",
            position="Разработчик",
            department="ИТ",
            hire_date="2026-01-01"

        )
        self.product = Product.objects.create(
            name="Смартфон",
            model="Nokia 3310",
            release_date="2010-10-20"
        )
        self.retail = Retail.objects.create(
            name="Nokia",
            email="email@email.com",
            country="Финляндия",
            city="Хельсинки",
            street="Уличная",
            house_number="1",
        )
        self.retail.products.add(self.product)
        self.client.force_authenticate(user=self.user)

    def test_retail_create(self):
        """Тест создания поставщика"""

        url = reverse(viewname="retail:retail-list")
        data = {
            "name": "Samsung",
            "email": "email@email.com",
            "country": "Корея",
            "city": "Пхеньян",
            "street": "Уличная",
            "house_number": "1",
        }
        self.retail.products.add(self.product)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Retail.objects.all().count(), 2)

    def test_retail_edit(self):
        """Тест изменения поставщика"""
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "name": "Apple",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.get(pk=self.retail.pk).name, "Apple")

    def test_retail_delete(self):
        """Тест удаления поставщика"""
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Retail.objects.all().count(), 0)

    def test_retail_filter(self):
        """Тест фильтра поставщика по стране. """

        url = reverse(viewname="retail:retail-list")
        self.retail = Retail.objects.create(
            name="Samsung",
            email="email@email.com",
            country="Корея",
            city="Пхеньян",
            street="Уличная",
            house_number="1",
        )
        response = self.client.get(url, data={'country': 'Корея'}, format="json")
        result = response.json()[0].get("id")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.all().count(), 2)
        self.assertEqual(result, 2)

    def test_debt_edit(self):
        """Тест изменения задолженности. """
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "debt": "1000",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.get(pk=self.retail.pk).debt, 0.00)

