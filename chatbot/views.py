"""
API views for the veterinary clinic chatbot.
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .agent import chat


@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request):
    """
    API endpoint for chat messages.
    
    Expects JSON body:
    {
        "message": "User's message",
        "history": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }
    
    Returns JSON:
    {
        "response": "Assistant's response",
        "success": true/false,
        "error": "Error message if any"
    }
    """
    try:
        # Parse request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON in request body"
            }, status=400)
        
        # Get message and history
        user_message = data.get("message", "").strip()
        chat_history = data.get("history", [])
        
        # Validate message
        if not user_message:
            return JsonResponse({
                "success": False,
                "error": "Message is required"
            }, status=400)
        
        # Limit message length
        if len(user_message) > 2000:
            return JsonResponse({
                "success": False,
                "error": "Message is too long (max 2000 characters)"
            }, status=400)
        
        # Limit history length to prevent abuse
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        # Get response from agent
        response = chat(user_message, chat_history)
        
        return JsonResponse({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        # Log error in production
        print(f"Chat view error: {e}")
        return JsonResponse({
            "success": False,
            "error": "Internal server error"
        }, status=500)
