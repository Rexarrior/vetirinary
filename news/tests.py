from django.test import TestCase
from django.urls import reverse

from .models import News


class NewsViewTests(TestCase):
    def test_list_and_detail_hide_unpublished_news(self):
        published = News.objects.create(title="Открытая", content="Текст")
        hidden = News.objects.create(title="Скрытая", content="Текст", is_published=False)

        response = self.client.get(reverse("news:news_list"))

        self.assertContains(response, published.title)
        self.assertNotContains(response, hidden.title)
        self.assertEqual(
            self.client.get(reverse("news:news_detail", args=[hidden.pk])).status_code,
            404,
        )

    def test_news_string_representation(self):
        news = News(title="Новость")

        self.assertEqual(str(news), "Новость")
