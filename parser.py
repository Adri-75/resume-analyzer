import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group() if match else "Not found"

def extract_education(text):
    degrees = ["bachelor", "master", "phd", "associate"]
    found = []
    for degree in degrees:
        if degree in text.lower():
            found.append(degree.title())
    return found or ["Not found"]

def parse_resume(text):
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Education": extract_education(text)
    }
