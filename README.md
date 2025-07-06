# 🧠 Resume Analyzer

An AI-powered web app that helps applicants evaluate how well their resume aligns with a given job description. Upload both PDFs, and receive a **semantic match score**, **natural-language feedback**, and **highlighted skills** pulled from the job post.

---

## ✨ Features

- ✅ Upload **resume** and **job description** as PDFs
- 🧠 Compute **AI-based match score** using BERT (MiniLM)
- 🧾 Get a **summary** of matched vs. missing concepts (NLP-based)
- 🖍️ **New!** Matched concepts from the job description are **highlighted** in the resume
- 🔍 **Resume parser** extracts:
  - Name
  - Email
  - Phone
  - Education

---

## 📦 Requirements

Install dependencies (compatible with Python 3.7+):

```bash
pip install "spacy<3.7" streamlit PyMuPDF sentence-transformers
python -m spacy download en_core_web_sm

---

## How to Run the App in Terminal

- streamlit run app.py
```
