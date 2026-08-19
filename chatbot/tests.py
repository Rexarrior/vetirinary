from unittest.mock import patch

from asgiref.sync import async_to_sync
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .agent import ChatPlan, _collect_sources, _normalize_history, get_llm


class ChatbotViewTests(TestCase):
    @patch("chatbot.views.chat", return_value="Здравствуйте!")
    def test_chat_endpoint_returns_agent_response(self, mocked_chat):
        response = self.client.post(
            reverse("chatbot:chat"),
            data={"message": "Где вы находитесь?", "history": []},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"success": True, "response": "Здравствуйте!"}
        )
        mocked_chat.assert_called_once_with("Где вы находитесь?", [])

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
