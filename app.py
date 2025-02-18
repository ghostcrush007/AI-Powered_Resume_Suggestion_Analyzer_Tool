import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from pdfminer.high_level import extract_text

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Function to extract text from a PDF
def extract_resume_text(uploaded_file):
    if uploaded_file is not None:
        text = extract_text(uploaded_file)
        return text
    return ""

# Function to get resume improvement suggestions
def get_resume_suggestions(resume_text, job_description):
    messages = [
        {
            "role": "system",
            "content": "You are a career coach and resume expert. Analyze the resume and job description, and provide suggestions to improve the resume for the given job."
        },
        {
            "role": "user",
            "content": f"Here is the resume text:\n{resume_text}\n\nHere is the job description:\n{job_description}\n\nProvide suggestions to improve the professional summary, work experience, projects, skills, and certifications sections to better align with the job description."
        }
    ]

    # Get completion from the model
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
        top_p=1,
        stream=False,
        stop=None
    )

    return completion.choices[0].message.content

# Streamlit UI
st.set_page_config(layout="wide", page_title="AI Resume Analyzer")

st.title("📄 AI-Powered Resume Analyzer")
st.write("Upload your resume and job description to get personalized improvement suggestions.")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job Description Input
job_description = st.text_area("Paste Job Description Here", height=250)

# Layout with two columns
col1, col2 = st.columns(2)

resume_text = ""

if uploaded_file is not None:
    resume_text = extract_resume_text(uploaded_file)

# Display Resume Content in Left Column
with col1:
    st.subheader("📜 Extracted Resume Content")
    if resume_text:
        st.text_area("Resume Content", resume_text, height=400)
    else:
        st.info("Upload a resume to see its content here.")

# Analyze Button
if st.button("🔍 Analyze"):
    if resume_text and job_description:
        with st.spinner("Analyzing resume..."):
            suggestions = get_resume_suggestions(resume_text, job_description)

        # Display Suggestions in Right Column
        with col2:
            st.subheader("💡 Resume Improvement Suggestions")
            st.write(suggestions)
    else:
        st.error("Please upload a resume and provide a job description.")

