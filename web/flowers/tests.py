from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from flowers.models import Flower, Bouquet, BouquetCategory


class FlowerAPITestCase(APITestCase):
    def setUp(self):
        self.flower = Flower.objects.create(name="Rose", price=10, can_be_sold_separately=True)
        self.bouquet = Bouquet.objects.create(name="Bouquet1", price=50)
        self.bouquet.flowers.add(self.flower)
        self.category = BouquetCategory.objects.create(name="Love")
        self.category.bouquets.add(self.bouquet)

    def test_flower_list(self):
        url = reverse("flowers:flower-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_flower_detail(self):
        url = reverse("flowers:flower-detail", args=[self.flower.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.flower.pk))

    def test_bouquet_list(self):
        url = reverse("flowers:bouquet-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_bouquet_detail(self):
        url = reverse("flowers:bouquet-detail", args=[self.bouquet.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.bouquet.pk))

    def test_bouquet_category_list(self):
        url = reverse("flowers:bouquet-category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_bouquet_category_detail(self):
        url = reverse("flowers:bouquet-category-detail", args=[self.category.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.category.pk))
