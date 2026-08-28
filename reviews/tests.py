from django.test import TestCase
from django.urls import reverse

from .models import Review


class ReviewViewTests(TestCase):
    def test_list_displays_only_published_reviews(self):
        Review.objects.create(author_name="Анна", rating=5, text="Спасибо", is_published=True)
        Review.objects.create(author_name="Скрытый", rating=3, text="Черновик", is_published=False)

        response = self.client.get(reverse("reviews:list"))

        self.assertContains(response, "Анна")
        self.assertNotContains(response, "Скрытый")
