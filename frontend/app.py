import streamlit as st
import requests

API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="SmartNotes AI",
    page_icon="📚",
    layout="centered"
)
st.markdown("""
    <style>
    h1 {
        white-space: nowrap;
        font-size: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📚 SmartNotes AI — Your Study Assistant")
st.caption("Ask questions from your notes and PDFs")

# Session state — For chat history 
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# Sidebar — PDF upload
with st.sidebar:
    st.header("PDF Upload ")
    uploaded_file = st.file_uploader(
        "Use your Pdf",
        type=["pdf"]
    )

    if uploaded_file and not st.session_state.pdf_uploaded:
        with st.spinner("PDF Processing ..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )}
            )
            result = response.json()

            if result["status"] == "success":
                st.success(f"Uploaded! {result['chunks']} chunks bane")
                st.session_state.pdf_uploaded = True
            else:
                st.error(f"Error: {result['message']}")

    if st.session_state.pdf_uploaded:
        st.info("PDF is ready  — Ask Questions")

    # Reset button
    if st.button("Reset"):
        st.session_state.messages = []
        st.session_state.pdf_uploaded = False
        st.rerun()

# Chat history dikhao
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question..."):
    if not st.session_state.pdf_uploaded:
        st.warning("Please upload a PDF from the sidebar first")
    else:
        # User message dikhao
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        # Answer lo
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": prompt}
                )
                result = response.json()

                if result["status"] == "success":
                    answer = result["answer"]
                    pages = result["source_pages"]

                    st.markdown(answer)

                    if pages:
                        st.caption(f"Source pages: {pages}")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error(f"Error: {result['message']}")