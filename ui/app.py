import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Document Q&A (RAG)", layout="centered")

st.title("Document Question Answering System")
st.write("Upload a document and ask questions based on its content.")

st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

if uploaded_file is not None:
    files = {"file": uploaded_file}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("Document uploaded and processed successfully")
        st.json(response.json())
    else:
        st.error("Failed to upload document")

# Question Section
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if not question:
        st.warning("Please enter a question")
    else:
        payload = {"question": question}
        response = requests.post(f"{BACKEND_URL}/ask", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.subheader("Answer")
            st.write(result["answer"])

            if result.get("sources"):
                st.subheader("Sources")
                for src in result["sources"]:
                    st.write(f"- {src}")
        else:
            st.error("Failed to get answer")
