import os
import sys
import streamlit as st

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Auto-detect and include virtual environment site-packages if running from global python
for venv_candidate in [
    os.path.join(BASE_DIR, "..", "venv", "Lib", "site-packages"),
    os.path.join(BASE_DIR, "venv", "Lib", "site-packages"),
    os.path.join(BASE_DIR, ".venv", "Lib", "site-packages"),
]:
    cand_abs = os.path.abspath(venv_candidate)
    if os.path.exists(cand_abs) and cand_abs not in sys.path:
        sys.path.insert(0, cand_abs)

from backend.app.classifier import classifier

# Configure Streamlit page layout and title
st.set_page_config(
    page_title="University Student Support Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern, Premium UI/UX
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Font & Smoothness */
html, body, [class*="css"], .stMarkdown, p, button, input {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

code, pre, .mono-font {
    font-family: 'JetBrains Mono', monospace !important;
}

/* App Background with ambient gradient */
.stApp {
    background: radial-gradient(circle at 50% 0%, rgba(79, 70, 229, 0.12) 0%, rgba(15, 23, 42, 0.98) 50%, #0b0f19 100%) !important;
    background-attachment: fixed !important;
    color: #f1f5f9;
}

/* Main Container Max-Width for readability */
.main .block-container {
    max-width: 960px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 6rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Hero Header Card */
.hero-container {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #3b82f6);
}

.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
}

.hero-pill.live {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.35);
    color: #6ee7b7;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

.hero-title {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    margin: 0 0 6px 0 !important;
    letter-spacing: -0.02em !important;
    color: #ffffff !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.gradient-text {
    background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 0.92rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.5;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0d1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0 16px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 18px;
}

.sidebar-logo {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.sidebar-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
}

.sidebar-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 16px;
}

.card-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 10px;
}

.topic-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.topic-pill {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #cbd5e1;
    font-size: 0.74rem;
    padding: 3px 8px;
    border-radius: 6px;
}

.sidebar-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 16px;
}

.stat-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 10px 6px;
    text-align: center;
}

.stat-number {
    font-size: 1.05rem;
    font-weight: 800;
    color: #818cf8;
}

.stat-label {
    font-size: 0.65rem;
    color: #64748b;
    margin-top: 2px;
}

/* Chat Message Styling */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 14px 18px !important;
    margin-bottom: 14px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    transition: all 0.2s ease-in-out;
}

/* User Message Bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(99, 102, 241, 0.08) 100%) !important;
    border: 1px solid rgba(129, 140, 248, 0.25) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Assistant Message Bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(22, 30, 49, 0.65) !important;
    border: 1px solid rgba(99, 102, 241, 0.18) !important;
    box-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

/* Modern Expander for Debug Info */
.streamlit-expanderHeader {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.2s ease;
}

.streamlit-expanderHeader:hover {
    color: #c7d2fe !important;
    border-color: rgba(99, 102, 241, 0.35) !important;
    background: rgba(30, 41, 59, 0.6) !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(99, 102, 241, 0.1) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 16px !important;
}

/* Quick Prompt Suggestions */
.suggestion-header {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    margin: 16px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Buttons Styling */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    background: rgba(30, 41, 59, 0.6) !important;
    color: #e2e8f0 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    border-color: #818cf8 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-1px);
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    background: rgba(15, 23, 42, 0.9) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #818cf8 !important;
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.25) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.3);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.6);
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_classifier():
    """Pre-load ML resources once on app launch."""
    classifier.load_resources()
    return classifier


# Initialize global classifier instance
bot_classifier = load_classifier()

# Sidebar UI
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🎓</div>
        <div>
            <div class="sidebar-title">Campus Assistant</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">University Support AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="card-title">Campus Topics</div>
        <div class="topic-grid">
            <span class="topic-pill">📅 Course Registration</span>
            <span class="topic-pill">🏢 Campus Facilities</span>
            <span class="topic-pill">📶 IT & Wi-Fi Support</span>
            <span class="topic-pill">💰 Financial Aid</span>
            <span class="topic-pill">📝 Exam Dates</span>
            <span class="topic-pill">⚖️ Academic Policies</span>
            <span class="topic-pill">🏡 Student Housing</span>
            <span class="topic-pill">🤝 Counseling</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-stats">
        <div class="stat-box">
            <div class="stat-number">200</div>
            <div class="stat-label">Verified FAQs</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">26</div>
            <div class="stat-label">Intents</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">100%</div>
            <div class="stat-label">Grounded</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Grounded Answers:** All answers are dataset-grounded and verified against university support records with strict dual-threshold filtering.")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        if "pending_prompt" in st.session_state:
            st.session_state.pending_prompt = None
        st.rerun()

# Main Chat Interface UI Header
st.markdown("""
<div class="hero-container">
    <div class="hero-badges">
        <span class="hero-pill live"><span class="pulse-dot"></span> System Online</span>
        <span class="hero-pill">⚡ all-MiniLM-L6-v2</span>
        <span class="hero-pill">🛡️ Strict Dataset Grounding</span>
    </div>
    <div class="hero-title">
        <span>University Student Support</span>
        <span class="gradient-text">Chatbot</span>
    </div>
    <div class="hero-subtitle">
        Ask questions about courses, registration, campus facilities, policies, financial aid, or IT support.
    </div>
</div>
""", unsafe_allow_html=True)


def display_debug_info(dbg: dict):
    """Renders debug information with modern metrics while preserving exact field text."""
    with st.expander("🛠️ Debug Information (AI Match Insights)", expanded=False):
        c1, c2 = st.columns(2)
        conf = dbg.get("confidence")
        sim = dbg.get("similarity")

        if dbg.get("is_general_conversation"):
            c1.metric("Intent Confidence", "1.0000", delta="Conversational Intent")
            c2.metric("System Layer", "General Chat", delta="Direct Match")
        else:
            if isinstance(conf, (int, float)):
                c1.metric("Intent Confidence", f"{conf:.4f}", delta="Pass (≥0.65)" if conf >= 0.65 else "Below Threshold")
            else:
                c1.metric("Intent Confidence", str(conf))

            if isinstance(sim, (int, float)):
                c2.metric("Question Similarity", f"{sim:.4f}", delta="Pass (≥0.60)" if sim >= 0.60 else "Fallback")
            else:
                c2.metric("Question Similarity", str(sim))

        st.markdown("---")
        st.write(f"**Question:** {dbg.get('question')}")
        st.write(f"**Predicted Intent:** {dbg.get('intent')}")
        st.write(f"**Intent Confidence:** {dbg.get('confidence')}")
        st.write(f"**Matched Question:** {dbg.get('matched_question')}")
        st.write(f"**Question Similarity:** {dbg.get('similarity')}")


# Initialize session state message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your University Student Support Assistant. How can I help you today?"
        }
    ]

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "debug" in message:
            display_debug_info(message["debug"])

# Suggestion Chips (displayed if conversation only has greeting)
if len(st.session_state.messages) <= 1:
    st.markdown('<div class="suggestion-header">💡 Frequently Asked Questions:</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    sample_queries = [
        "How do I add a course to my schedule?",
        "When is the library open on weekends?",
        "How to connect to campus Wi-Fi?",
        "Are there scholarships for international students?"
    ]
    for idx, query_text in enumerate(sample_queries):
        col = c1 if idx % 2 == 0 else c2
        if col.button(f"👉 {query_text}", key=f"chip_{idx}", use_container_width=True):
            st.session_state.pending_prompt = query_text
            st.rerun()

# User prompt input handling
prompt = st.chat_input("Type your question here...")

user_prompt = None
if prompt:
    user_prompt = prompt
elif st.session_state.get("pending_prompt"):
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_prompt:
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Predict response using existing ML classifier
    with st.spinner("Searching for answer..."):
        result = bot_classifier.predict(user_prompt)
        response_text = result["response"]

    # Append and display assistant response with debug info
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "debug": result
    })
    with st.chat_message("assistant"):
        st.markdown(response_text)
        display_debug_info(result)
    st.rerun()
