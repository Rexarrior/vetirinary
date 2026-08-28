from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicAndAdminSmokeTests(TestCase):
    def test_public_pages_render(self):
        route_names = [
            "home",
            "services:list",
            "services:prices",
            "reviews:list",
            "news:news_list",
            "contacts:contacts",
            "contacts:contact_us",
            "contacts:contact_success",
            "about:about",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "{{")
                self.assertNotContains(response, "{%")
                self.assertNotContains(response, "{ {")

    def test_admin_requires_authentication(self):
        response = self.client.get(reverse("admin:index"))

        self.assertRedirects(
            response,
            f"{reverse('admin:login')}?next={reverse('admin:index')}",
        )

    def test_superuser_can_open_admin(self):
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
