import streamlit as st
import PyPDF2
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract skills from text
def extract_skills(text):
    doc = nlp(text)
    skills = set()
    common_skills = {"python", "java", "machine learning", "data science", "sql", "excel", "power bi", "deep learning", "nlp"}  # Extend with more skills
    
    for token in doc:
        if token.text.lower() in common_skills:
            skills.add(token.text.lower())
    return skills

# Streamlit UI
st.title("Resume Scanner & Skill Matcher Python App")
st.write("Upload your resume and paste the job description to find matching skills.")
st.subheader("Made by [Shahbaz Mehmood]")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description Here")

if uploaded_file and job_description:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text)
    job_doc = nlp(job_description)
    
    job_skills = extract_skills(job_doc.text)
    matched_skills = resume_skills.intersection(job_skills)
    
    st.subheader("Extracted Skills from Resume:")
    st.write(resume_skills)
    
    st.subheader("Matched Skills with Job Description:")
    st.write(matched_skills)
    
    st.subheader("Skill Match Percentage:")
    match_percentage = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
    st.write(f"{match_percentage:.2f}%")
