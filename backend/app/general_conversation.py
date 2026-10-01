"""General Conversation Layer for CampusBot.

This module provides a manual, rule-based conversational intent detection
and response system for greetings, small talk, acknowledgements, and casual queries.

This layer executes BEFORE the ML intent classifier and dataset vector search to ensure
normal conversational messages do not trigger the unknown-answer fallback.
"""

import re
from typing import Optional, Dict, Any


# ---------------------------------------------------------------------------
# 1. Configurable General Conversation Responses
# ---------------------------------------------------------------------------
GENERAL_RESPONSES: Dict[str, str] = {
    "greeting": (
        "Hello! I'm CampusBot, your University Student Support Assistant. "
        "How can I help you today?"
    ),
    "how_are_you": (
        "I'm doing great, thank you for asking! "
        "How can I assist you with your campus queries today?"
    ),
    "identity": (
        "I'm CampusBot, an AI assistant designed to help students with campus-related "
        "information including course registration, facilities, exams, policies, and financial aid."
    ),
    "capabilities": (
        "I can help you with questions about course registration, campus facilities, "
        "academic policies, financial aid, IT & Wi-Fi support, exam dates, housing, "
        "and student counseling. Feel free to ask anything!"
    ),
    "thanks": (
        "You're very welcome! Let me know if you need help with anything else."
    ),
    "goodbye": (
        "Goodbye! Have a great day and best of luck with your studies!"
    ),
    "acknowledgement": (
        "Got it! Let me know whenever you have any campus-related questions."
    ),
    "positive": (
        "Awesome! I'm glad to hear that. How else can I assist you?"
    ),
    "good_night": (
        "Good night! Take care and rest well!"
    ),
    "courtesy": (
        "It's a pleasure to assist you! Feel free to ask any questions about campus life."
    ),
    "apology": (
        "No worries at all! How can I help you?"
    ),
    "laughter": (
        "Haha! Glad to chat. What campus questions can I help you with?"
    ),
}


# ---------------------------------------------------------------------------
# 2. Text Normalization Function
# ---------------------------------------------------------------------------
def normalize_text(text: str) -> str:
    """Normalize user input for robust conversational matching.
    
    Operations performed:
    - Lowercase conversion
    - Leading/trailing whitespace stripping
    - Normalization of common repeated characters (e.g. 'hellooo' -> 'hello', 'hiii' -> 'hi')
    - Removal of extraneous punctuation while keeping alphanumeric content
    - Collapsing multiple spaces into a single space
    
    Example:
        "  HELLO!!!  " -> "hello"
        "hiiiii there???" -> "hi there"
    """
    if not text or not isinstance(text, str):
        return ""

    # Convert to lowercase
    normalized = text.lower().strip()

    # Normalize specific elongated greetings and words
    # e.g., 'hiii' -> 'hi', 'heyyy' -> 'hey', 'hellooo' -> 'hello', 'byeee' -> 'bye'
    normalized = re.sub(r'\bhi+\b', 'hi', normalized)
    normalized = re.sub(r'\bhey+\b', 'hey', normalized)
    normalized = re.sub(r'\bhello+\b', 'hello', normalized)
    normalized = re.sub(r'\bbye+\b', 'bye', normalized)
    normalized = re.sub(r'\bok+\b', 'ok', normalized)
    normalized = re.sub(r'\bthx+\b', 'thanks', normalized)
    normalized = re.sub(r'\bha(ha)+\b', 'haha', normalized)

    # General repeated character reduction (3+ repeats of any character -> 1)
    # e.g., 'soooo' -> 'so', 'pleaaase' -> 'please'
    normalized = re.sub(r'(.)\1{2,}', r'\1', normalized)

    # Replace punctuation with spaces (retain alphanumeric and spaces)
    normalized = re.sub(r'[^\w\s]', ' ', normalized)

    # Collapse multiple consecutive whitespace into a single space
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


# ---------------------------------------------------------------------------
# 3. Intent Detection Function
# ---------------------------------------------------------------------------
# Conversational target regex patterns with strict anchors and boundaries
# to prevent false positives with campus questions.
CONVERSATIONAL_PATTERNS = [
    # GREETING
    (
        "greeting",
        re.compile(
            r"^(hello|hi|hey|heya|howdy|greetings|good\s+(morning|afternoon|evening))"
            r"(\s+(there|bro|dude|bot|campusbot|campus\s+bot|assistant|friend|everyone|all|team))?$",
            re.IGNORECASE
        )
    ),
    # HOW_ARE_YOU
    (
        "how_are_you",
        re.compile(
            r"^(how\s+(are\s+you|are\s+u|r\s+you|r\s+u|are\s+you\s+doing|do\s+you\s+do|is\s+it\s+going|are\s+things))"
            r"(\s+(doing|today|there|bro|campusbot))?$",
            re.IGNORECASE
        )
    ),
    # IDENTITY
    (
        "identity",
        re.compile(
            r"^(who\s+are\s+(you|u)|what\s+are\s+(you|u)|what\s+is\s+your\s+name|who\s+is\s+campusbot|"
            r"tell\s+me\s+about\s+yourself|who\s+made\s+you|who\s+created\s+you)$",
            re.IGNORECASE
        )
    ),
    # CAPABILITIES
    (
        "capabilities",
        re.compile(
            r"^(what\s+can\s+(you|u)\s+do|how\s+can\s+(you|u)\s+help(\s+me)?|what\s+do\s+(you|u)\s+do|"
            r"what\s+are\s+your\s+capabilities|how\s+to\s+use\s+this(\s+bot)?|help\s+me|help)$",
            re.IGNORECASE
        )
    ),
    # THANKS
    (
        "thanks",
        re.compile(
            r"^(thank(s|\s+you|\s+u)(\s+(so\s+much|a\s+lot|very\s+much))?|thx|ty|"
            r"many\s+thanks)(\s+(campusbot|bro|there))?$",
            re.IGNORECASE
        )
    ),
    # GOODBYE
    (
        "goodbye",
        re.compile(
            r"^(bye(\s+bye)?|goodbye|good\s+bye|see\s+you(\s+later|\s+soon)?|cya|catch\s+you\s+later|"
            r"take\s+care|talk\s+to\s+you\s+later)(\s+(campusbot|bro|there))?$",
            re.IGNORECASE
        )
    ),
    # ACKNOWLEDGEMENT
    (
        "acknowledgement",
        re.compile(
            r"^(ok|okay|alright|all\s+right|got\s+it|gotcha|fine|understood|sure|k|kk|"
            r"noted)(\s+(thanks|thank\s+you|campusbot))?$",
            re.IGNORECASE
        )
    ),
    # POSITIVE
    (
        "positive",
        re.compile(
            r"^(great|awesome|cool|nice|that\s*s\s+great|thats\s+great|superb|wonderful|"
            r"perfect|amazing|sounds\s+good)(\s+(job|work|thanks|campusbot))?$",
            re.IGNORECASE
        )
    ),
    # GOOD_NIGHT
    (
        "good_night",
        re.compile(
            r"^(good\s*night|night\s*night|have\s+a\s+good\s*night)(\s+(campusbot|all))?$",
            re.IGNORECASE
        )
    ),
    # COURTESY
    (
        "courtesy",
        re.compile(
            r"^(welcome|you\s*re\s+welcome|you\s+are\s+welcome|no\s+problem|my\s+pleasure|"
            r"nice\s+to\s+meet\s+you|pleased\s+to\s+meet\s+you)$",
            re.IGNORECASE
        )
    ),
    # APOLOGY
    (
        "apology",
        re.compile(
            r"^(sorry|i\s*m\s+sorry|my\s+bad|apologies|excuse\s+me)$",
            re.IGNORECASE
        )
    ),
    # LAUGHTER
    (
        "laughter",
        re.compile(
            r"^(haha+|hehe+|lol|lmao|rofl)$",
            re.IGNORECASE
        )
    ),
]


def detect_general_intent(text: str) -> Optional[str]:
    """Detect general conversational intent from user input.
    
    Returns the intent category name (e.g. 'greeting', 'thanks') if matched,
    or None if the query should proceed to dataset/ML similarity search.
    
    Safeguards:
    Uses strict regex patterns to prevent false positives. For example:
    - 'Who is the director of the college?' -> None (proceeds to dataset)
    - 'What can I do if I fail a course?' -> None (proceeds to dataset)
    - 'Who are you?' -> 'identity' (general conversation)
    """
    cleaned = normalize_text(text)
    if not cleaned:
        return None

    for intent, pattern in CONVERSATIONAL_PATTERNS:
        if pattern.match(cleaned):
            return intent

    return None


# ---------------------------------------------------------------------------
# 4. Response Retrieval Function
# ---------------------------------------------------------------------------
def get_general_response(intent: str) -> Optional[str]:
    """Retrieve pre-defined response for a detected general conversation intent."""
    return GENERAL_RESPONSES.get(intent)


# ---------------------------------------------------------------------------
# 5. Handler Function for Chatbot Pipeline
# ---------------------------------------------------------------------------
def handle_general_conversation(user_question: str) -> Optional[Dict[str, Any]]:
    """Check if the user question is a general conversation message.
    
    If yes:
        Returns a standardized dictionary matching the classifier predict format:
        {
            "question": user_question,
            "intent": intent,
            "confidence": 1.0,
            "matched_question": "General Conversation Layer",
            "similarity": 1.0,
            "response": response
        }
    If no:
        Returns None, signaling the pipeline to continue to ML / dataset search.
    """
    intent = detect_general_intent(user_question)
    if intent:
        response = get_general_response(intent)
        if response:
            return {
                "question": user_question,
                "intent": intent,
                "confidence": 1.0,
                "matched_question": "General Conversation Layer",
                "similarity": 1.0,
                "response": response,
                "is_general_conversation": True
            }
    return None
