# Resume Analyzer
Using modern AI and NLP tools that allows users (applicants) to upload a resume and job description (PDFs), compare them using semantic similarity, and receive a match score with an explanation and resume feedback.

---

## Features

- Upload resume and job description as PDFs
- Compute AI-based match score using BERT (MiniLM)
- NLP-based summary: what’s matched, what’s missing
- Resume parser: extract name, email, phone, and education
- Get warnings if key resume fields are missing

---

## Requirements

- pip install streamlit PyMuPDF spacy sentence-transformers
- python -m spacy download en_core_web_sm

---

## How to Run the App in Terminal

- streamlit run app.py