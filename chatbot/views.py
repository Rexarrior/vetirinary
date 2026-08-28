"""API views for the public veterinary clinic chatbot."""

import hashlib
import json
import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


def chat(user_message, chat_history=None):
    """Load the relatively heavy NOOA runtime only when chat is used."""
    from .agent import chat as run_chat

    return run_chat(user_message, chat_history)


def _rate_limit_identifiers(request):
    client_ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR", "unknown")
    yield "ip", client_ip

    csrf_cookie = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
    if csrf_cookie:
        yield "browser", csrf_cookie


def _is_rate_limited(request):
    limit = settings.CHATBOT_RATE_LIMIT_REQUESTS
    timeout = settings.CHATBOT_RATE_LIMIT_WINDOW_SECONDS

    for scope, identifier in _rate_limit_identifiers(request):
        digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()
        key = f"chatbot-rate:{scope}:{digest}"
        if cache.add(key, 1, timeout=timeout):
            continue
        try:
            request_count = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=timeout)
            request_count = 1
        if request_count > limit:
            return True
    return False


def _error(message, status):
    return JsonResponse({"success": False, "error": message}, status=status)


def _record_metrics(outcome, duration_ms):
    """Store aggregate operational counters without request or client data."""
    timeout = 30 * 24 * 60 * 60
    for key, initial_value in (
        ("chatbot-metrics:requests", 1),
        (f"chatbot-metrics:outcome:{outcome}", 1),
        ("chatbot-metrics:duration-ms-total", duration_ms),
    ):
        if cache.add(key, initial_value, timeout=timeout):
            continue
        try:
            cache.incr(key, initial_value)
        except (ValueError, TypeError):
            cache.set(key, initial_value, timeout=timeout)


def _validated_history(value):
    if not isinstance(value, list):
        raise ValueError("History must be a list")
    if len(value) > settings.CHATBOT_MAX_HISTORY_ITEMS:
        raise ValueError("History contains too many messages")

    history = []
    total_characters = 0
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("History items must be objects")
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            raise ValueError("History item has an invalid role or content")
        content = content.strip()
        if len(content) > settings.CHATBOT_MAX_MESSAGE_LENGTH:
            raise ValueError("History message is too long")
        total_characters += len(content)
        if total_characters > settings.CHATBOT_MAX_HISTORY_CHARACTERS:
            raise ValueError("History is too large")
        if content:
            history.append({"role": role, "content": content})
    return history


@require_POST
def chat_view(request):
    """Process one bounded, CSRF-protected chatbot request."""
    started_at = time.monotonic()
    outcome = "server_error"
    try:
        if request.content_type != "application/json":
            outcome = "unsupported_media_type"
            return _error("Content-Type must be application/json", 415)

        if _is_rate_limited(request):
            outcome = "rate_limited"
            response = _error("Слишком много запросов. Попробуйте через минуту.", 429)
            response["Retry-After"] = str(settings.CHATBOT_RATE_LIMIT_WINDOW_SECONDS)
            return response

        try:
            data = json.loads(request.body)
        except RequestDataTooBig:
            outcome = "payload_too_large"
            return _error("Request body is too large", 413)
        except (json.JSONDecodeError, UnicodeDecodeError):
            outcome = "invalid_json"
            return _error("Invalid JSON in request body", 400)

        if not isinstance(data, dict):
            outcome = "invalid_payload"
            return _error("JSON body must be an object", 400)

        raw_message = data.get("message", "")
        if not isinstance(raw_message, str):
            outcome = "invalid_message"
            return _error("Message must be a string", 400)
        user_message = raw_message.strip()
        if not user_message:
            outcome = "empty_message"
            return _error("Message is required", 400)
        if len(user_message) > settings.CHATBOT_MAX_MESSAGE_LENGTH:
            outcome = "message_too_long"
            return _error("Message is too long", 400)

        try:
            chat_history = _validated_history(data.get("history", []))
        except ValueError as exc:
            outcome = "invalid_history"
            return _error(str(exc), 400)

        response = chat(user_message, chat_history)
        outcome = "success"
        return JsonResponse({"success": True, "response": response})
    except Exception:
        logger.exception("Unhandled chatbot view error")
        return _error("Internal server error", 500)
    finally:
        duration_ms = round((time.monotonic() - started_at) * 1000)
        try:
            _record_metrics(outcome, duration_ms)
        except Exception:
            logger.exception("Failed to record chatbot aggregate metrics")
        logger.info("chatbot_request outcome=%s duration_ms=%d", outcome, duration_ms)
