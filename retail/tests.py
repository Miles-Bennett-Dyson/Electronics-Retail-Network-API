from django.contrib import admin
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from retail.admin import RetailAdmin
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
        self.retail_2 = Retail.objects.create(
            name="TOSHIBA",
            email="email@email.com",
            country="Япония",
            city="Токио",
            street="Уличная",
            house_number="1",
        )
        self.retail.products.add(self.product)
        self.retail_2.products.add(self.product)
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
        self.assertEqual(Retail.objects.all().count(), 3)

    def test_retail_edit(self):
        """Тест изменения поставщика"""
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "name": "Apple",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.get(pk=self.retail.pk).name, "Apple")

    def test_self_identification_supplier(self):
        """Тест указания поставщиком самого себя """
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "supplier": self.retail.pk,
        }
        response = self.client.patch(url, data, format="json")
        self.retail.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Нельзя себя же, указывать поставщиком!', response.data['non_field_errors'])
        self.assertEqual(self.retail.supplier, None)

    def test_supplier_correctness(self):
        """Тест правильного указания поставщика. """
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "supplier": self.retail_2.pk,
        }
        response = self.client.patch(url, data, format="json")
        self.retail.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.retail.supplier, self.retail_2)

    def test_cyclic_hierarchy(self):
        """Тест циклической иерархии при указании поставщика. """
        url = reverse(viewname="retail:retail-detail", args=(self.retail_2.pk,))
        self.retail.supplier = self.retail_2
        self.retail.save()
        data = {
            "supplier": self.retail.pk,
        }
        response = self.client.patch(url, data, format="json")
        self.retail.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Циклическая иерархия!', response.data['non_field_errors'])
        self.assertEqual(self.retail_2.supplier, None)

    def test_retail_delete(self):
        """Тест удаления поставщика"""
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Retail.objects.all().count(), 1)

    def test_retail_filter(self):
        """Тест фильтра поставщика по стране. """

        url = reverse(viewname="retail:retail-list")
        response = self.client.get(url, data={'country': 'Япония'}, format="json")
        result = response.json()[0].get("id")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.all().count(), 2)
        self.assertEqual(result, 2)

    def test_retail_filter_important_country(self):
        """Тест фильтра поставщика по несуществующей стране. """

        url = reverse(viewname="retail:retail-list")
        response = self.client.get(url, data={'country': 'Венера'}, format="json")
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.all().count(), 2)
        self.assertEqual(result, [])

    def test_debt_edit(self):
        """Тест изменения задолженности. """
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "debt": "1000",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.get(pk=self.retail.pk).debt, 0.00)

    def test_debt_reset_via_admin_panel(self):
        """Тест удаления задолженности через админ панель. """
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        self.retail.debt = 1000
        self.retail.save()
        self.retail_2.debt = 2000
        self.retail_2.save()
        qs = Retail.objects.filter(pk=1)
        admin_obj = RetailAdmin(model=Retail, admin_site=admin.site)
        admin_obj.message_user = lambda request, message: None
        admin_obj.debt_reset(request=None, queryset=qs)
        self.retail.refresh_from_db()
        self.retail_2.refresh_from_db()
        self.assertEqual(self.retail.debt, 0)
        self.assertEqual(self.retail_2.debt, 2000)

    def test_retail_active_employee(self):
        """Тест доступа к API только активным сотрудникам. """
        self.user.is_active = False
        self.user.save()
        url = reverse(viewname="retail:retail-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
