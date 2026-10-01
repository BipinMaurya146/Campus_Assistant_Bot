# University Student Support Chatbot

An AI-powered, dataset-grounded chatbot built with Streamlit and Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`) to provide precise, verified answers to university student queries.

## Architecture

```text
Streamlit UI (streamlit_app.py)
        ↓
backend/app/classifier.py
        ↓
SentenceTransformer (all-MiniLM-L6-v2)
        ↓
Intent Prototype Matching (model/intent_prototypes.pkl)
        ↓
Intent Confidence Threshold (0.65)
        ↓
Dataset Question Similarity Search (data/AI-Powered Chatbot.xlsx - Chatbot_Student_Support.csv)
        ↓
Question Similarity Threshold (0.80)
        ↓
Exact Dataset "Bot Response" Retrieval
```

## Features
- **Strict Dataset Grounding**: Answers are retrieved exclusively from the verified 200-row university student support dataset. Zero hallucinated or LLM-generated responses.
- **Two-Tier Thresholding**:
  - Intent Confidence Threshold: `0.65`
  - Question Similarity Threshold: `0.80`
- **Pre-computed Embedding Cache**: Pre-computes and caches 200 question embeddings upon startup using `@st.cache_resource` for high performance.
- **Debug Panel**: Displays question metadata, predicted intent, confidence score, and similarity score inside an expandable debug panel for each message.

## Project Structure

```text
University_Student_Chatbot/
│
├── streamlit_app.py                      # Main Streamlit user interface
├── README.md                             # Project documentation
├── requirements.txt                      # Python dependencies
│
├── backend/
│   └── app/
│       ├── __init__.py                   # Package initialization
│       └── classifier.py                 # Core ML intent & dataset similarity classifier
│
├── data/
│   └── AI-Powered Chatbot.xlsx - Chatbot_Student_Support.csv # 200-row Q&A dataset
│
├── model/
│   └── intent_prototypes.pkl             # Pre-computed 26 384-d intent prototype vectors
│
└── notebook/
    └── Chatbot_Student_Support_Cleaned.ipynb # Data cleaning & model training notebook
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run streamlit_app.py
```
