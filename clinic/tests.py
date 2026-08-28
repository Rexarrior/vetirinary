from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse


class ReadinessViewTests(TestCase):
    def test_readiness_reports_healthy_database(self):
        response = self.client.get(reverse("readiness"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    @patch("clinic.health.connection.cursor", side_effect=DatabaseError)
    def test_readiness_reports_database_failure(self, mocked_cursor):
        response = self.client.get(reverse("readiness"))

        self.assertEqual(response.status_code, 503)
        self.assertJSONEqual(response.content, {"status": "unhealthy"})
        mocked_cursor.assert_called_once_with()

    def test_readiness_rejects_non_get_requests(self):
        response = self.client.post(reverse("readiness"))

        self.assertEqual(response.status_code, 405)
