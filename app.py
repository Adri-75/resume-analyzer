import streamlit as st
import fitz  # PyMuPDF
from analyzer import compute_match_score, generate_summary, highlight_matches
from parser import parse_resume

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("🧠 AI-Powered Resume Analyzer")

st.markdown("Upload your resume and a job description to see how well they match.")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    return ""

if resume_file and job_file:
    resume_text = extract_text_from_pdf(resume_file)
    parsed_data = parse_resume(resume_text)

    st.subheader("🧾 Resume Details:")
    for key, value in parsed_data.items():
        display_value = value if isinstance(value, str) else ", ".join(value)
        st.write(f"**{key}:** {display_value}")
        if display_value == "Not found":
            st.warning(f"⚠️ Your resume is missing a {key.lower()} — consider adding it.")

    job_text = extract_text_from_pdf(job_file)

    st.subheader("🔍 Analysis Results:")

    match_score = compute_match_score(resume_text, job_text)
    summary_text = generate_summary(resume_text, job_text, match_score)

    highlighted_resume = highlight_matches(resume_text, job_text)

    st.subheader("💡 Skill Matches Highlighted in Resume:")
    st.markdown(highlighted_resume, unsafe_allow_html=True)

    st.metric(label="Match Score", value=f"{match_score}%")
    st.markdown(summary_text)

else:
    st.info("Please upload both a resume and job description in PDF format to continue.")
