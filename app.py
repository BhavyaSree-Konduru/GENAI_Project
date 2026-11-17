import streamlit as st
from rag_service import get_answer
from config import *

st.set_page_config(
    page_title="GenAI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 100%
    );
}

.main-title{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    color:#60a5fa;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:30px;
}

[data-testid="stChatMessage"]{
    border-radius:15px;
    padding:10px;
}

[data-testid="stSidebar"]{
    background-color:#1e293b;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    st.info(f"Model: {LLM_MODEL}")

    st.info(f"Top K: {TOP_K}")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ---------------------------
# Header
# ---------------------------

st.markdown(
    """
    <div class='main-title'>
        🤖 GenAI Assistant
    </div>

    <div class='sub-title'>
        Ask questions from your knowledge base
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Chat History
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ---------------------------
# Chat Input
# ---------------------------

question = st.chat_input(
    "Ask anything..."
)

# ---------------------------
# Ask Question
# ---------------------------

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

        with st.spinner(
            "Searching knowledge base..."
        ):

            result = get_answer(question)

        answer = result["answer"]

        st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.expander("📚 Sources"):

            for doc in result["sources"]:

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                st.markdown(
                    f"""
                    🔹 **File:** {source}

                    🔹 **Page:** {page}
                    """
                )

        with st.expander(" Retrieved Context"):

            for idx, doc in enumerate(
                result["sources"],
                start=1
            ):

                st.markdown(
                    f"### Chunk {idx}"
                )

                st.write(
                    doc.page_content
                )

                st.divider()