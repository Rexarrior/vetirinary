from django.test import TestCase
from django.urls import reverse

from .models import ContactSubmission


class ContactFormTests(TestCase):
    def test_valid_submission_is_saved_and_redirected(self):
        response = self.client.post(
            reverse("contacts:contact_us"),
            {
                "name": "Анна",
                "email": "anna@example.com",
                "phone": "+7 900 000-00-00",
                "subject": "Запись",
                "message": "Нужна консультация",
            },
        )

        self.assertRedirects(response, reverse("contacts:contact_success"))
        self.assertTrue(ContactSubmission.objects.filter(email="anna@example.com").exists())

    def test_invalid_submission_is_not_saved(self):
        response = self.client.post(
            reverse("contacts:contact_us"),
            {"name": "Анна", "email": "bad-email", "subject": "Запись"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "email", "Введите правильный адрес электронной почты."
        )
        self.assertEqual(ContactSubmission.objects.count(), 0)
