import os
from langchain.chat_models import ChatTogether
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 🔑 API Keys
os.environ["TOGETHER_API_KEY"] = "45fc0ac4cf54d42e0bcaf9d4cd2c57de87ad5a39afc4c29d32923e44706b9a4f"
os.environ["LANGCHAIN_PROJECT"] = "cv-matcher"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"  # Optional

# 💬 Prompt template
template = """
You are a CV adaptation assistant for job applications. Given a resume and job description, generate a fully rewritten resume tailored to the job, using the following formula:

1. Write a personalized "About Me" summary: include years of experience, industries, and 2–3 measurable achievements.
2. Rewrite work experience using inverted pyramid structure, with focus on OUTCOME over output (impact on KPIs, profits, time etc).
3. One-page clear & scannable format including:
   - Personal info at top (name, phone, email, LinkedIn)
   - One unique title
   - Years only (no months)
   - Company description if relevant
4. Bottom: education, languages, volunteering, skills.

Avoid:
- Generic or long-winded sentences
- Output without outcome
- Unfocused roles
- Messy formatting

Think like an HR reviewer, hiring manager, and ATS algorithm. Identify what’s missing, complete it, and output the final English CV draft as plain text.

---

📄 Resume:
{resume}

📌 Job Description:
{job}

---
Final CV:
"""

prompt = ChatPromptTemplate.from_template(template)
model = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.4)
chain = prompt | model | StrOutputParser()

def match_resume_to_job(resume_text, job_text):
    return chain.invoke({"resume": resume_text, "job": job_text})

