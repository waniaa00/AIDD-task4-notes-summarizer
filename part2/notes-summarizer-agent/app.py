import streamlit as st
import asyncio
from tools import extract_text_from_pdf, save_to_memory
from agent import run_agent

st.set_page_config(page_title="Study Notes Agent", page_icon="📚", layout="wide")

st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload a PDF to generate summaries and quizzes powered by Gemini 2.0 Flash")

# Step 1: Upload PDF
st.header("Step 1: Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if "pdf_text" not in st.session_state or st.session_state.get("last_file") != uploaded_file.name:
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.session_state["pdf_text"] = pdf_text
            st.session_state["last_file"] = uploaded_file.name
            
            # Save to memory
            save_to_memory(uploaded_file.name, {"size": uploaded_file.size})
        
        st.success(f"✅ Extracted {len(pdf_text)} characters from {uploaded_file.name}")
    
    # Step 2: Generate Summary
    st.header("Step 2: Generate Summary")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        layout = st.selectbox("Display Layout", ["container", "card", "block"])
    
    if st.button("Generate Summary", type="primary"):
        with st.spinner("Generating summary..."):
            prompt = f"Summarize the following PDF text into clear, student-friendly notes:\n\n{st.session_state['pdf_text']}"
            summary = asyncio.run(run_agent(prompt))
            st.session_state["summary"] = summary
    
    if "summary" in st.session_state:
        if layout == "card":
            with st.container(border=True):
                st.markdown("### 📝 Summary")
                st.markdown(st.session_state["summary"])
        elif layout == "block":
            st.markdown("### 📝 Summary")
            st.markdown(st.session_state["summary"])
        else:  # container
            with st.container():
                st.markdown("### 📝 Summary")
                st.markdown(st.session_state["summary"])
    
    # Step 3: Generate Quiz
    st.header("Step 3: Generate Quiz")
    
    if st.button("Create Quiz", type="primary"):
        with st.spinner("Generating quiz..."):
            prompt = f"Generate a quiz based ONLY on the following full PDF text. Produce MCQs or mixed-style questions:\n\n{st.session_state['pdf_text']}"
            quiz = asyncio.run(run_agent(prompt))
            st.session_state["quiz"] = quiz
    
    if "quiz" in st.session_state:
        st.markdown("### 🎯 Quiz")
        st.markdown(st.session_state["quiz"])
else:
    st.info("👆 Please upload a PDF file to get started")
