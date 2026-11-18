import streamlit as st
from rag_service import get_answer
from config import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GenAI Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
APP BACKGROUND
===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 100%
    );
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {
    background-color: #111827;
}

/* =====================================================
CONFIG CARDS
===================================================== */

.config-card{
    background:#1e293b;
    color:white;
    padding:15px;
    border-radius:12px;
    margin-bottom:12px;
    border:1px solid #334155;
}

/* =====================================================
HEADER
===================================================== */

.main-title{
    font-size:42px;
    font-weight:700;
    text-align:center;
    color:#60a5fa;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}

/* =====================================================
CHAT MESSAGES
===================================================== */

[data-testid="stChatMessage"] {
    background:#1e293b;
    border:1px solid #334155;
    border-radius:16px;
    padding:14px;
    margin-bottom:12px;
}

[data-testid="stChatMessageContent"] p {
    color:white !important;
    font-size:16px !important;
    line-height:1.8 !important;
}

/* =====================================================
GLOBAL TEXT
===================================================== */

.stMarkdown,
.stText,
p,
span,
label {
    color:white;
}

/* =====================================================
SOURCE BOX
===================================================== */

.source-box{
    background:#0f172a;
    color:white;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    border-left:4px solid #60a5fa;
}

/* =====================================================
CHUNK BOX
===================================================== */

.chunk-box{
    background:#0f172a;
    color:white;
    padding:15px;
    border-radius:10px;
    margin-bottom:12px;
    white-space:pre-wrap;
    border:1px solid #334155;
}

/* =====================================================
EXPANDER
===================================================== */

details{
    background:#1e293b;
    border-radius:10px;
    padding:5px;
}

summary{
    color:white !important;
}

/* =====================================================
BUTTONS
===================================================== */

.stButton > button{
    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px;
}

.stButton > button:hover{
    background:#1d4ed8;
}

/* =====================================================
CHAT INPUT (FIXED)
===================================================== */

/* Main chat container */

[data-testid="stChatInput"] {
    background:#1e293b !important;
    border:1px solid #334155 !important;
    border-radius:12px !important;
}

/* Actual input field */

[data-testid="stChatInput"] textarea {
    background:#1e293b !important;
    color:white !important;
    caret-color:white !important;
}

/* Placeholder */

[data-testid="stChatInput"] textarea::placeholder {
    color:#94a3b8 !important;
}

/* BaseWeb override */

[data-baseweb="textarea"] textarea {
    background:#1e293b !important;
    color:white !important;
    caret-color:white !important;
}

/* Newer Streamlit versions */

.stChatInputContainer textarea {
    background:#1e293b !important;
    color:white !important;
    caret-color:white !important;
}

/* Universal override */

textarea,
input {
    color:white !important;
    caret-color:white !important;
}

textarea::placeholder,
input::placeholder {
    color:#94a3b8 !important;
}

/* Remove white box */

[data-baseweb="textarea"] {
    background:#1e293b !important;
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <h1 style="color:white;">
            ⚙️ Configuration
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="config-card">
            <strong>🤖 Model</strong><br>
            {LLM_MODEL}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="config-card">
            <strong>📚 Top K</strong><br>
            {TOP_K}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">
        🤖 GenAI Assistant
    </div>

    <div class="sub-title">
        Ask questions from your knowledge base
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input("Ask anything...")

# =====================================================
# PROCESS QUESTION
# =====================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "🔍 Searching knowledge base..."
            ):
                result = get_answer(question)

            answer = ""

            if isinstance(result, dict):

                if "answer" in result:
                    answer = result["answer"]

                elif "result" in result:
                    answer = result["result"]

                else:
                    answer = str(result)

            else:
                answer = str(result)

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # =================================================
            # SOURCES
            # =================================================

            if (
                isinstance(result, dict)
                and "sources" in result
                and result["sources"]
            ):

                with st.expander("📚 Sources"):

                    for doc in result["sources"]:

                        source = doc.metadata.get(
                            "source",
                            "Unknown"
                        )

                        page = doc.metadata.get(
                            "page",
                            "N/A"
                        )

                        st.markdown(
                            f"""
                            <div class="source-box">
                                📄 <b>File:</b> {source}<br>
                                📍 <b>Page:</b> {page}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # =================================================
            # RETRIEVED CONTEXT
            # =================================================

            if (
                isinstance(result, dict)
                and "sources" in result
                and result["sources"]
            ):

                with st.expander(
                    "🔍 Retrieved Context"
                ):

                    for idx, doc in enumerate(
                        result["sources"],
                        start=1
                    ):

                        st.markdown(
                            f"### Chunk {idx}"
                        )

                        st.markdown(
                            f"""
                            <div class="chunk-box">
                            {doc.page_content}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )