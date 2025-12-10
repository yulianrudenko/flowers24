from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_payload = {
            "email": "newuser@mail.com",
            "password": "12345",
            "first_name": "New",
            "last_name": "User",
            "phone": "+48123456789",
        }
        self.user = User.objects.create_user(**self.user_payload)
        self.client.force_authenticate(user=self.user)

    def test_user_register_success(self):
        self.user.delete()

        response = self.client.post(reverse('users:register'), self.user_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_payload["email"]).exists())

    def test_user_register_password_is_hashed(self):
        self.user.delete()

        response = self.client.post(reverse('users:register'), self.user_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_payload["email"])
        self.assertNotEqual(user.password, self.user_payload["password"])
        self.assertTrue(user.check_password(self.user_payload["password"]))

    def test_user_detail_get(self):
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_profile_get(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_profile_patch(self):
        url = reverse("users:profile")
        response = self.client.patch(url, {"first_name": "Jane"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")

    def test_user_profile_delete(self):
        url = reverse("users:profile")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
