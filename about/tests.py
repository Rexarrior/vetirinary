from django.test import TestCase
from django.urls import reverse

from .models import Veterinarian


class AboutViewTests(TestCase):
    def test_about_displays_only_active_veterinarians(self):
        Veterinarian.objects.create(
            name="Доктор Айболит", position="Терапевт", bio="Опыт", is_active=True
        )
        Veterinarian.objects.create(
            name="Скрытый врач", position="Терапевт", bio="Опыт", is_active=False
        )

        response = self.client.get(reverse("about:about"))

        self.assertContains(response, "Доктор Айболит")
        self.assertNotContains(response, "Скрытый врач")
