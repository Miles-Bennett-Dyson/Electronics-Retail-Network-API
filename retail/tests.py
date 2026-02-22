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

    def test_habit_edit(self):
        """Тест изменения поставщика"""
        url = reverse(viewname="retail:retail-detail", args=(self.retail.pk,))
        data = {
            "name": "Apple",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Retail.objects.get(pk=self.retail.pk).name, "Apple")
    #
    # def test_changes_another_user(self):
    #     """Тест изменения привычки другим пользователем."""
    #     self.user_2 = User.objects.create(email="test2@test.com")
    #     self.client.force_authenticate(user=self.user_2)
    #     url = reverse(viewname="habits:habit-detail", kwargs={"pk": self.habit.pk})
    #     data = {
    #         "duration": datetime.timedelta(minutes=1),
    #     }
    #     response = self.client.patch(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(Habits.objects.get(place="Бассейн").duration, datetime.timedelta(seconds=120))
    #
    # def test_habit_delete(self):
    #     """Тест удаления привычки"""
    #     url = reverse(viewname="habits:habit-detail", args=(self.habit.pk,))
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Habits.objects.all().count(), 0)
    #
    # def test_is_pleasure_and_reward(self):
    #     """Тест одновременного указания вознаграждения и приятной привычки."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 1,
    #         "reward": "Печенье",
    #         "is_pleasure": True,
    #         "duration": datetime.timedelta(minutes=2),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "У приятной привычки не может быть вознаграждения или связанной привычки!"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)
    #
    # def test_is_pleasure_and_related_habit(self):
    #     """Тест одновременного указания приятной привычки и связанной привычки."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 1,
    #         "related_habit": self.habit.pk,
    #         "is_pleasure": True,
    #         "duration": datetime.timedelta(minutes=2),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "У приятной привычки не может быть вознаграждения или связанной привычки!"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)
    #
    # def test_periodicity(self):
    #     """Тест создания привычки с периодом больше 7."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 8,
    #         "reward": "Печенье",
    #         "duration": datetime.timedelta(minutes=2),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "Нельзя выполнять привычку реже, чем 1 раз в 7 дней!"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)
    #
    # def test_not_related_habit_and_not_reward(self):
    #     """Тест создания привычки без вознаграждения или связанной привычки."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 7,
    #         "duration": datetime.timedelta(minutes=2),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "Необходимо указать вознаграждение ИЛИ связанную привычку"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)
    #
    # def test_related_habit_and_reward(self):
    #     """Тест одновременного указания вознаграждения и связанной привычки."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 1,
    #         "reward": "Печенье",
    #         "related_habit": self.habit.pk,
    #         "duration": datetime.timedelta(minutes=2),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "Можно указать только вознаграждение ИЛИ связанную привычку"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)
    #
    # def test_duration(self):
    #     """Тест указания времени выполнения привычки."""
    #     url = reverse(viewname="habits:habit-list")
    #     data = {
    #         "place": "Парк",
    #         "time": datetime.time(20, 30),
    #         "action": "Гулять",
    #         "periodicity": 1,
    #         "reward": "Печенье",
    #         "related_habit": self.habit.pk,
    #         "duration": datetime.timedelta(minutes=6),
    #         "is_public": True,
    #         "owner": self.user.pk,
    #     }
    #     response = self.client.post(url, data, format="json")
    #     validation_error_text = response.json().get("non_field_errors")[0]
    #     expected_text = "Время на выполнение не должно быть более 120 секунд!"
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(validation_error_text, expected_text)