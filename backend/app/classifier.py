import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from backend.app.general_conversation import (
    handle_general_conversation,
    normalize_text,
    detect_general_intent,
    get_general_response,
)

INTENT_THRESHOLD = 0.65
ANSWER_THRESHOLD = 0.60
DEFAULT_FALLBACK = "Sorry, I don't have an answer for this question."


class IntentClassifier:
    """ML Intent Classifier using SentenceTransformer, prototype vectors, and dataset question similarity."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        base_dir: str = None
    ):
        if base_dir is None:
            # Default path pointing to workspace root directory
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.base_dir = base_dir
        self.model_dir = os.path.join(base_dir, "model")
        self.data_dir = os.path.join(base_dir, "data")
        self.model_name = model_name

        self.model = None
        self.intent_prototypes = {}
        self.dataset_df = None
        self.question_embeddings = None
        self._is_loaded = False

    def load_resources(self):
        """Load SentenceTransformer model, intent prototypes, and CSV dataset with pre-computed question embeddings."""
        if self._is_loaded:
            return

        prototypes_path = os.path.join(self.model_dir, "intent_prototypes.pkl")
        csv_path = os.path.join(self.data_dir, "AI-Powered Chatbot.xlsx - Chatbot_Student_Support.csv")

        if not os.path.exists(prototypes_path):
            raise FileNotFoundError(f"Prototypes file not found at: {prototypes_path}")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset CSV file not found at: {csv_path}")

        # 1. Load SentenceTransformer model
        self.model = SentenceTransformer(self.model_name)

        # 2. Load saved 26 intent prototype vectors
        with open(prototypes_path, "rb") as f:
            self.intent_prototypes = pickle.load(f)

        # 3. Load dataset CSV containing User Message, Intent, and Bot Response columns
        self.dataset_df = pd.read_csv(csv_path)

        # 4. Pre-compute and cache normalized embeddings for all 200 "User Message" dataset questions
        questions = self.dataset_df["User Message"].tolist()
        self.question_embeddings = self.model.encode(
            questions,
            normalize_embeddings=True
        )

        self._is_loaded = True

    def predict(self, user_question: str) -> dict:
        """Process user question through the response pipeline:
        
        Priority 1: Check manual general conversation layer (greetings, small talk, etc.).
                    If matched, returns immediately without triggering ML search or fallback.
        Priority 2: Pre-computed Intent Prototype matching via SentenceTransformer embeddings.
        Priority 3: Filtered dataset question cosine similarity search.
        Priority 4: Dual threshold verification (Intent >= 0.65, Similarity >= 0.60).
        Priority 5: Fallback response if confidence is below threshold.
        """
        # =====================================================================
        # Step 1: Manual General Conversation Layer (Priority 1)
        # =====================================================================
        general_match = handle_general_conversation(user_question)
        if general_match is not None:
            return general_match

        # =====================================================================
        # Step 2: ML Model & Dataset Retrieval (Priority 2 & 3)
        # =====================================================================
        if not self._is_loaded:
            self.load_resources()

        # a. Generate 384-dimensional normalized embedding for user question
        user_embedding = self.model.encode(
            [user_question],
            normalize_embeddings=True
        )

        # b. Calculate cosine similarity with ALL intent prototypes
        prototype_scores = {}
        for intent, prototype in self.intent_prototypes.items():
            similarity = cosine_similarity(
                user_embedding,
                prototype.reshape(1, -1)
            )[0][0]
            prototype_scores[intent] = float(similarity)

        # c. Select highest-scoring intent
        predicted_intent = max(prototype_scores, key=prototype_scores.get)
        confidence = round(prototype_scores[predicted_intent], 4)

        # d. If intent confidence < 0.65
        if confidence < INTENT_THRESHOLD:
            return {
                "question": user_question,
                "intent": "unknown",
                "confidence": confidence,
                "matched_question": None,
                "similarity": confidence,
                "response": DEFAULT_FALLBACK
            }

        # e. Otherwise filter the dataset safely by index alignment
        intent_df = self.dataset_df[
            self.dataset_df["Intent"] == predicted_intent
        ].copy()

        if len(intent_df) == 0:
            return {
                "question": user_question,
                "intent": "unknown",
                "confidence": confidence,
                "matched_question": None,
                "similarity": 0.0,
                "response": DEFAULT_FALLBACK
            }

        intent_questions = intent_df["User Message"].tolist()
        intent_responses = intent_df["Bot Response"].tolist()
        intent_embeddings = self.question_embeddings[intent_df.index.to_numpy()]

        # f. Compare user embedding ONLY against questions belonging to predicted intent
        similarities = cosine_similarity(
            user_embedding,
            intent_embeddings
        )[0]

        best_position = np.argmax(similarities)
        best_similarity = round(float(similarities[best_position]), 4)
        matched_question = intent_questions[best_position]
        matched_response = intent_responses[best_position]

        # h. If question similarity < 0.80
        if best_similarity < ANSWER_THRESHOLD:
            return {
                "question": user_question,
                "intent": "unknown",
                "confidence": confidence,
                "matched_question": None,
                "similarity": best_similarity,
                "response": DEFAULT_FALLBACK
            }

        # i. If similarity >= 0.80: return exact Bot Response from matched dataset row
        return {
            "question": user_question,
            "intent": predicted_intent,
            "confidence": confidence,
            "matched_question": matched_question,
            "similarity": best_similarity,
            "response": matched_response
        }

    def chatbot(self, user_question: str) -> dict:
        """Alias to predict method following the full priority pipeline."""
        return self.predict(user_question)


# Global classifier instance
classifier = IntentClassifier()


def chatbot(user_question: str) -> dict:
    """Main chatbot pipeline entrypoint.
    
    Priority Flow:
    1. USER INPUT -> normalize_text(user_question)
    2. Check manual general conversation layer (detect_general_intent / get_general_response)
    3. If general conversation matched -> return predefined friendly response
    4. Otherwise, run Intent Prototype matching and Dataset question similarity search
    5. If similarity threshold met -> return exact dataset answer
    6. If no match -> return default fallback: "Sorry, I don't have an answer for this question."
    """
    return classifier.predict(user_question)




