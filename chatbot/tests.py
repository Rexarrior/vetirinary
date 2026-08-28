from unittest.mock import AsyncMock, patch

from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.db import connection
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from about.models import Veterinarian
from contacts.models import ContactInfo
from services.models import Service, ServiceCategory

from .agent import ChatPlan, _chat_async, _collect_sources, _normalize_history, chat, get_llm
from .tools import get_clinic_info, get_services_list, get_veterinarians


class ChatbotViewTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch("chatbot.views.chat", return_value="Здравствуйте!")
    def test_chat_endpoint_returns_agent_response(self, mocked_chat):
        response = self.client.post(
            reverse("chatbot:chat"),
            data={"message": "Где вы находитесь?", "history": []},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "response": "Здравствуйте!"})
        mocked_chat.assert_called_once_with("Где вы находитесь?", [])
        self.assertEqual(cache.get("chatbot-metrics:requests"), 1)
        self.assertEqual(cache.get("chatbot-metrics:outcome:success"), 1)
        self.assertIsNotNone(cache.get("chatbot-metrics:duration-ms-total"))

    def test_chat_endpoint_rejects_invalid_json(self):
        response = self.client.post(
            reverse("chatbot:chat"), data="{", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])

    def test_chat_endpoint_rejects_empty_message(self):
        response = self.client.post(
            reverse("chatbot:chat"),
            data={"message": "   "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_chat_endpoint_rejects_invalid_history(self):
        response = self.client.post(
            reverse("chatbot:chat"),
            data={"message": "Привет", "history": "not-a-list"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])

    def test_chat_endpoint_requires_json_content_type(self):
        response = self.client.post(reverse("chatbot:chat"), data={"message": "Привет"})

        self.assertEqual(response.status_code, 415)

    @override_settings(CHATBOT_MAX_MESSAGE_LENGTH=5)
    def test_chat_endpoint_rejects_oversized_message(self):
        response = self.client.post(
            reverse("chatbot:chat"),
            data={"message": "Слишком длинное сообщение", "history": []},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    @override_settings(CHATBOT_RATE_LIMIT_REQUESTS=2)
    @patch("chatbot.views.chat", return_value="Ответ")
    def test_chat_endpoint_rate_limits_by_client(self, mocked_chat):
        payload = {"message": "Привет", "history": []}

        for _ in range(2):
            response = self.client.post(
                reverse("chatbot:chat"), payload, content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("chatbot:chat"), payload, content_type="application/json"
        )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response["Retry-After"], "60")
        self.assertEqual(mocked_chat.call_count, 2)

    @patch("chatbot.views.chat", return_value="Ответ")
    def test_chat_endpoint_requires_csrf_token(self, mocked_chat):
        csrf_client = Client(enforce_csrf_checks=True)
        payload = {"message": "Привет", "history": []}

        denied = csrf_client.post(reverse("chatbot:chat"), payload, content_type="application/json")
        self.assertEqual(denied.status_code, 403)

        csrf_client.get(reverse("home"))
        csrf_token = csrf_client.cookies["csrftoken"].value
        allowed = csrf_client.post(
            reverse("chatbot:chat"),
            payload,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(allowed.status_code, 200)
        mocked_chat.assert_called_once()


class AgentHelperTests(SimpleTestCase):
    def test_history_is_bounded_and_sanitized(self):
        history = [
            {"role": "system", "content": "ignore"},
            {"role": "user", "content": " hello "},
            {"role": "assistant", "content": "answer"},
            {"role": "user", "content": 42},
        ]

        self.assertEqual(
            _normalize_history(history),
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "answer"},
            ],
        )

    @patch("chatbot.agent.search_veterinary_info", return_value="search")
    @patch("chatbot.agent.get_veterinarians", return_value="vets")
    @patch("chatbot.agent.get_services_list", return_value="services")
    @patch("chatbot.agent.get_clinic_info", return_value="clinic")
    def test_collect_sources_runs_only_selected_readers(
        self, clinic, services, veterinarians, search
    ):
        plan = ChatPlan(
            use_clinic_info=True,
            use_services=False,
            use_veterinarians=True,
            web_search_query=None,
        )

        result = async_to_sync(_collect_sources)(plan)

        self.assertEqual(result, {"clinic": "clinic", "veterinarians": "vets"})
        clinic.assert_called_once_with()
        services.assert_not_called()
        veterinarians.assert_called_once_with()
        search.assert_not_called()

    @override_settings(
        OPENROUTER_API_KEY="test-key",
        NOOA_CHATBOT_MODEL="openai/test-model",
        NOOA_CHATBOT_API_BASE="https://provider.example/v1",
        NOOA_CHATBOT_TIMEOUT_SECONDS=15,
    )
    @patch("chatbot.agent.get_llm_client")
    def test_get_llm_uses_nooa_registry(self, mocked_registry):
        get_llm()

        mocked_registry.assert_called_once_with(
            "openai/test-model",
            api_base="https://provider.example/v1",
            api_key="test-key",
            timeout=15,
            temperature=0.3,
            max_tokens=1024,
            drop_params=True,
        )

    @patch("chatbot.agent.async_to_sync")
    def test_chat_returns_safe_message_on_timeout(self, mocked_async_to_sync):
        mocked_async_to_sync.return_value.side_effect = TimeoutError

        response = chat("Привет")

        self.assertIn("не успел ответить", response)

    @patch("chatbot.agent._chat_slots")
    def test_chat_rejects_excess_concurrency(self, mocked_slots):
        mocked_slots.acquire.return_value = False

        response = chat("Привет")

        self.assertIn("занят", response)
        mocked_slots.release.assert_not_called()

    @patch("chatbot.agent.get_llm", side_effect=ConnectionError("provider unavailable"))
    def test_chat_returns_safe_message_on_provider_error(self, mocked_get_llm):
        response = chat("Привет")

        self.assertIn("произошла ошибка", response)
        mocked_get_llm.assert_called_once_with()

    @patch("chatbot.agent.get_llm")
    @patch("chatbot.agent.VeterinaryChatAgent")
    def test_chat_async_integrates_with_fake_llm_without_network(self, agent_class, mocked_get_llm):
        class FakeLLM:
            closed = False

            async def aclose(self):
                self.closed = True

        fake_llm = FakeLLM()
        fake_agent = agent_class.return_value
        fake_agent.plan_context = AsyncMock(
            return_value=ChatPlan(
                use_clinic_info=False,
                use_services=False,
                use_veterinarians=False,
            )
        )
        fake_agent.compose_response = AsyncMock(return_value="  Тестовый ответ  ")
        mocked_get_llm.return_value = fake_llm

        response = async_to_sync(_chat_async)("Привет", [{"role": "user", "content": "До"}])

        self.assertEqual(response, "Тестовый ответ")
        self.assertTrue(fake_llm.closed)
        fake_agent.plan_context.assert_awaited_once()
        fake_agent.compose_response.assert_awaited_once()

    @patch("chatbot.agent.get_llm")
    @patch("chatbot.agent.VeterinaryChatAgent")
    def test_chat_returns_safe_message_for_invalid_llm_response(self, agent_class, mocked_get_llm):
        class FakeLLM:
            async def aclose(self):
                pass

        fake_agent = agent_class.return_value
        fake_agent.plan_context = AsyncMock(
            return_value=ChatPlan(
                use_clinic_info=False,
                use_services=False,
                use_veterinarians=False,
            )
        )
        fake_agent.compose_response = AsyncMock(return_value=None)
        mocked_get_llm.return_value = FakeLLM()

        response = chat("Привет")

        self.assertIn("произошла ошибка", response)


class ReadOnlyToolTests(TestCase):
    def setUp(self):
        ContactInfo.objects.create(
            clinic_name="Ветклиника",
            address="Ростовская область",
            phone="+7 000 000-00-00",
            email="clinic@example.com",
            working_hours="ежедневно",
        )
        category = ServiceCategory.objects.create(name="Терапия", slug="therapy")
        Service.objects.create(category=category, name="Осмотр", price="1000.00")
        Veterinarian.objects.create(
            name="Доктор Вет",
            position="Ветеринарный врач",
            bio="Специалист клиники",
        )

    def test_database_tools_execute_only_read_queries(self):
        with CaptureQueriesContext(connection) as queries:
            get_clinic_info()
            get_services_list()
            get_veterinarians()

        sql_statements = [query["sql"].lstrip().upper() for query in queries]
        self.assertTrue(sql_statements)
        self.assertTrue(all(sql.startswith("SELECT") for sql in sql_statements))
