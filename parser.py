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
    # List of degree keywords and abbreviations to look for
    degree_keywords = [
        "bachelor", "master", "phd", "associate",
        "b.s", "b.a", "m.s", "m.a", "ph.d", "bs", "ba", "ms", "ma", "doctorate"
    ]
    
    found = []
    # Lowercase text for case-insensitive search
    lowered = text.lower()
    
    # Simple approach: check if any keyword is in text
    for degree in degree_keywords:
        # Use word boundaries or dots optional (handle both "b.s" and "bs")
        pattern = re.compile(r'\b' + degree.replace('.', r'\.?') + r'\b', re.IGNORECASE)
        if pattern.search(lowered):
            found.append(degree.upper().replace('.', ''))  # Normalize display
    
    if found:
        return found
    
    # If none found, try to extract lines that start with "education"
    lines = text.splitlines()
    for line in lines:
        if 'education' in line.lower():
            return [line.strip()]
    
    return ["Not found"]

def parse_resume(text):
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Education": extract_education(text)
    }
