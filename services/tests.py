from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Service, ServiceCategory


class ServiceViewTests(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Терапия", slug="therapy")
        self.active_service = Service.objects.create(
            category=self.category, name="Осмотр", price=Decimal("1500.00")
        )
        Service.objects.create(
            category=self.category,
            name="Скрытая услуга",
            price=Decimal("500.00"),
            is_active=False,
        )

    def test_category_displays_only_active_services(self):
        response = self.client.get(reverse("services:category", args=[self.category.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.active_service.name)
        self.assertNotContains(response, "Скрытая услуга")

    def test_inactive_category_returns_not_found(self):
        self.category.is_active = False
        self.category.save(update_fields=["is_active"])

        response = self.client.get(reverse("services:category", args=[self.category.slug]))

        self.assertEqual(response.status_code, 404)
