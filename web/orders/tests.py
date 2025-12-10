from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from flowers.models import Flower
from orders.models import Order, OrderItem, Payment
from orders.services import create_order_item
from users.models import User


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@mail.com",
            password="1234",
            first_name="Alice",
            last_name="Jones",
            phone="+48123456789",
        )
        self.client.force_authenticate(user=self.user)
        self.flower = Flower.objects.create(
            name="Tulipan", price=5, can_be_sold_separately=True
        )
        self.order = Order.objects.create(user=self.user)

    def test_order_list(self):
        url = reverse("orders:order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_order_create(self):
        url = reverse("orders:order-list")
        response = self.client.post(url)
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED]
        )

    def test_order_item_merge_logic(self):
        OrderItem.objects.create(order=self.order, flower=self.flower, quantity=2)
        item = create_order_item(order=self.order, flower=self.flower, quantity=3)
        self.assertEqual(item.quantity, 5)

    def test_order_pay(self):
        OrderItem.objects.create(order=self.order, flower=self.flower, quantity=1)
        self.order.status = Order.Status.WAITING_PAYMENT
        self.order.save()

        url = reverse("orders:order-pay", args=[self.order.pk])
        response = self.client.post(url, {"method": Payment.Method.BLIK.value})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PAID)
        self.assertTrue(Payment.objects.filter(order=self.order).exists())
