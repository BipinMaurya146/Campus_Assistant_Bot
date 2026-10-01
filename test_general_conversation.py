import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Auto-detect venv
for venv_candidate in [
    os.path.join(BASE_DIR, "..", "venv", "Lib", "site-packages"),
    os.path.join(BASE_DIR, "venv", "Lib", "site-packages"),
]:
    cand_abs = os.path.abspath(venv_candidate)
    if os.path.exists(cand_abs) and cand_abs not in sys.path:
        sys.path.insert(0, cand_abs)

from backend.app.classifier import chatbot, classifier
from backend.app.general_conversation import (
    normalize_text,
    detect_general_intent,
    get_general_response,
    handle_general_conversation
)

print("--- TEST 1: Normalization ---")
tests_norm = [
    ("  HELLO!!!  ", "hello"),
    ("hiiiii there???", "hi there"),
    ("how  are   you??", "how are you"),
    ("  What CAN you DO?!  ", "what can you do")
]
for raw, expected in tests_norm:
    res = normalize_text(raw)
    assert res == expected, f"Expected '{expected}', got '{res}'"
    print(f"OK: '{raw}' -> '{res}'")

print("\n--- TEST 2: General Conversation Queries ---")
tests_conv = [
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("hii", "greeting"),
    ("hiii", "greeting"),
    ("hellooo", "greeting"),
    ("  HELLO!!!  ", "greeting"),
    ("hello bro", "greeting"),
    ("hey campusbot", "greeting"),
    ("hi there", "greeting"),
    ("good morning", "greeting"),
    ("good afternoon", "greeting"),
    ("good evening", "greeting"),
    ("how are you?", "how_are_you"),
    ("how are you doing?", "how_are_you"),
    ("how r u?", "how_are_you"),
    ("how r you", "how_are_you"),
    ("who are you?", "identity"),
    ("what are you?", "identity"),
    ("what is your name", "identity"),
    ("what can you do?", "capabilities"),
    ("how can you help me", "capabilities"),
    ("thanks", "thanks"),
    ("thank you", "thanks"),
    ("thank you so much", "thanks"),
    ("okay", "acknowledgement"),
    ("ok", "acknowledgement"),
    ("alright", "acknowledgement"),
    ("bye", "goodbye"),
    ("goodbye", "goodbye"),
    ("see you", "goodbye"),
    ("nice to meet you", "courtesy"),
    ("good night", "good_night"),
    ("welcome", "courtesy"),
    ("sorry", "apology"),
    ("that's great", "positive"),
    ("great", "positive"),
    ("cool", "positive"),
    ("awesome", "positive"),
    ("haha", "laughter"),
    ("lol", "laughter")
]
for query, expected_intent in tests_conv:
    out = chatbot(query)
    assert out.get("is_general_conversation") is True, f"Failed for '{query}': not marked general conv"
    assert out.get("intent") == expected_intent, f"Expected '{expected_intent}', got '{out.get('intent')}' for '{query}'"
    print(f"OK: '{query}' -> intent={out.get('intent')}, response={out.get('response')[:45]}...")

print("\n--- TEST 3: False Positive Safeguards ---")
tests_negative = [
    "Who is the director of the college?",
    "What can I do if I fail a course?",
    "How do I add a course to my schedule?",
    "When is the library open on weekends?",
    "Are there scholarships for international students?"
]
for q in tests_negative:
    intent = detect_general_intent(q)
    assert intent is None, f"False positive detected for '{q}': returned {intent}"
    print(f"OK: '{q}' correctly bypassed general layer (intent=None)")

print("\n--- TEST 4: Dataset Retrieval Still Works ---")
classifier.load_resources()
res_dataset = chatbot("How do I add a course to my schedule?")
assert res_dataset.get("intent") == "course_registration", f"Dataset intent mismatch: {res_dataset}"
assert "Registration" in res_dataset.get("response") or "course" in res_dataset.get("response").lower(), f"Response mismatch: {res_dataset}"
print(f"OK: Dataset query answered correctly: {res_dataset.get('response')[:60]}...")

print("\nALL 4 TEST SUITES PASSED SUCCESSFULLY!")
