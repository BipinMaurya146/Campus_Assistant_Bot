"""University Student Support Chatbot Backend Application Package."""

from backend.app.classifier import classifier, chatbot, IntentClassifier
from backend.app.general_conversation import (
    normalize_text,
    detect_general_intent,
    get_general_response,
    handle_general_conversation,
    GENERAL_RESPONSES,
)

__all__ = [
    "classifier",
    "chatbot",
    "IntentClassifier",
    "normalize_text",
    "detect_general_intent",
    "get_general_response",
    "handle_general_conversation",
    "GENERAL_RESPONSES",
]
