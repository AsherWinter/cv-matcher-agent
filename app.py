import streamlit as st
from cv_agent_together_fixed import match_resume_to_job

st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("🤖 AI Resume Matcher")
st.markdown("התאם את קורות החיים שלך למשרה בלחיצת כפתור – מותאם ל־HR ולמערכות ATS מבוססות AI.")

with st.form("matcher_form"):
    resume_text = st.text_area("📄 קורות חיים (באנגלית)", height=300)
    job_text = st.text_area("📌 תיאור משרה", height=300)
    submitted = st.form_submit_button("🚀 בצע התאמה")

if submitted:
    if not resume_text.strip() or not job_text.strip():
        st.warning("נא למלא גם את קורות החיים וגם את תיאור המשרה.")
    else:
        with st.spinner("מכין גרסה מותאמת..."):
            try:
                result = match_resume_to_job(resume_text, job_text)
                st.success("🎯 קורות החיים הותאמו בהצלחה!")
                st.text_area("📄 גרסה מומלצת", result, height=500)
            except Exception as e:
                st.error(f"שגיאה בעיבוד: {e}")
