import streamlit as st
from pdfminer.high_level import extract_text
import docx
import os
import groq

# Set your Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    return extract_text(pdf_file)

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to analyze resume using Groq LLM
def analyze_resume_with_groq(resume_text, job_desc):
    prompt = f"""
    You are an AI assistant helping candidates evaluate their resume against a job description. 
    Your task is to assign a relevance score (0-100) and provide **well-structured feedback**.  

    **Feedback Format:**  
    - **SCORE:** <numeric_score>/100  
    - **DETAILED FEEDBACK:** Clearly formatted, covering all resume sections.  
      Each section should:
        - State **what’s missing**.
        - Provide **1-2 full examples** of how to improve it.  

    **Example Format for Each Section:**  
    ### **Professional Summary**  
    - **What’s Missing:** The summary lacks mention of distributed systems and multi-threaded programming.  
    - **Suggested Summary Example:**  
      _"Experienced Software Engineer specializing in distributed systems and multi-threaded programming. Designed and optimized large-scale services using C++ and Golang, improving efficiency by 40%."_  

    ### **Skills**  
    - **What’s Missing:** The resume does not include experience with NoSQL databases.  
    - **Suggested Skills Example:**  
      _"- NoSQL Databases: MongoDB, Cassandra."_  

    **Now analyze the following resume against the job description:**  

    **Job Description:**  
    {job_desc}  

    **Candidate's Resume:**  
    {resume_text}  

    Provide the feedback in the structured format above.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    output_text = response.choices[0].message.content
    return output_text

# Streamlit UI
def main():
    st.title("AI-Powered Resume Scoring System (Groq)")

    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste the job description here:")

    if uploaded_file and job_description:
        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            extracted_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format")
            return

        # Analyze resume with Groq
        analysis_result = analyze_resume_with_groq(extracted_text, job_description)

        # Display results
        st.subheader("Resume Analysis Result")
        st.markdown(analysis_result)

if __name__ == "__main__":
    main()
