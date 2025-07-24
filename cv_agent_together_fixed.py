
import streamlit as st
from langsmith import traceable
from fpdf import FPDF
import os
from langchain.chat_models import ChatOpenAI

# הגדר API Keys
st.sidebar.title("🔧 הגדרות")
together_key = st.sidebar.text_input("🔑 Together API Key", type="password")
langsmith_key = st.sidebar.text_input("📊 LangSmith API Key (לא חובה)", type="password")

if together_key:
    os.environ["OPENAI_API_KEY"] = together_key
    os.environ["OPENAI_API_BASE"] = "https://api.together.xyz/v1"
if langsmith_key:
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key
    os.environ["LANGCHAIN_PROJECT"] = "cv-matcher-agent"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

st.title("🤖 התאמת קורות חיים למשרה – Together AI (Fixed)")
st.markdown("הזן טקסטים של מועמד ושל משרה, ותקבל התאמה מיידית (בחינם, ללא OpenAI)")

resume_text = st.text_area("✍️ קורות חיים")
job_text = st.text_area("📄 תיאור משרה")

@traceable(name="Compare CV and Job (Together API)")
def match_resume_to_job(resume, job):
    llm = ChatOpenAI(
        temperature=0.2,
        max_tokens=1024,
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        openai_api_key=together_key,
        openai_api_base="https://api.together.xyz/v1"
    )
    prompt = f"""
השווה בין קורות החיים למשרה הבאה.
החזר אחוז התאמה מ-0 עד 100 + נימוק קצר.

קורות חיים:
{resume}

משרה:
{job}
    """
    return llm.invoke(prompt).content

import unicodedata

def sanitize_text(text):
    return ''.join(c for c in text if unicodedata.category(c)[0] != 'So')  # מסיר אמוג'ים ותווים מיוחדים

def create_pdf(resume):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_text = sanitize_text(resume)
    for line in safe_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=1)
    file_path = "final_resume.pdf"
    pdf.output(file_path)
    return file_path


if st.button("✨ בצע התאמה"):
    if not together_key:
        st.error("אנא הזן Together API Key")
    elif not resume_text or not job_text:
        st.warning("אנא מלא גם קורות חיים וגם משרה")
    else:
        with st.spinner("בודק התאמה עם Together AI..."):
            result = match_resume_to_job(resume_text, job_text)
            st.success("התאמה הושלמה!")
            st.markdown(f"**תוצאה:**\n\n{result}")
            pdf_path = create_pdf(resume_text)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 הורד PDF", f, file_name="resume.pdf")
