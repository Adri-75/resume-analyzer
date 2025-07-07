from sentence_transformers import SentenceTransformer, util
from difflib import get_close_matches
import spacy
import re
import unicodedata

SECTION_HEADERS = {
    "requirements", "responsibilities", "preferred", "skills",
    "summary", "qualifications", "education"
}

# Load models once
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load('en_core_web_sm')

def compute_match_score(resume_text, job_text):
    """
    Computes a semantic similarity score between resume and job description text.
    Returns a float percentage (0–100)
    """
    if not resume_text or not job_text:
        return 0.0

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_embedding, job_embedding).item()
    return round(similarity * 100, 2)

def normalize_text(text):
    # Lowercase, strip spaces, normalize unicode
    return unicodedata.normalize('NFKC', text.strip().lower())

def extract_combined_noun_phrases(text):
    doc = nlp(text)
    noun_chunks = list(doc.noun_chunks)
    combined_phrases = set()

    i = 0
    while i < len(noun_chunks):
        phrase = noun_chunks[i].text
        j = i + 1
        while j < len(noun_chunks) and noun_chunks[j].start == noun_chunks[j - 1].end:
            phrase += " " + noun_chunks[j].text
            j += 1
        combined_phrases.add(normalize_text(phrase))
        i = j
    return combined_phrases

def extract_entities_and_proper_nouns(text):
    doc = nlp(text)
    entities = set(normalize_text(ent.text) for ent in doc.ents)
    proper_nouns = set(normalize_text(token.text) for token in doc if token.pos_ == "PROPN" and len(token.text.strip()) > 1)
    return entities.union(proper_nouns)

def extract_dynamic_concepts(text):
    concepts = set()
    concepts.update(extract_combined_noun_phrases(text))
    concepts.update(extract_entities_and_proper_nouns(text))
    return concepts

def deduplicate_phrases(phrases):
    unique = []
    for phrase in phrases:
        if not get_close_matches(phrase, unique, n=1, cutoff=0.85):
            unique.append(phrase)
    return unique


def generate_summary(resume_text, job_text, score):
    """
    Generates a natural-language summary of the resume-job match.
    """
    resume_concepts = extract_dynamic_concepts(resume_text)
    job_concepts = extract_dynamic_concepts(job_text)

    matched = resume_concepts.intersection(job_concepts)
    missing = job_concepts.difference(resume_concepts)

    # Normalize and filter
    matched_clean = {c.lower().strip() for c in matched}
    missing_clean = {
        c.lower().strip()
        for c in missing
        if len(c.split()) > 1 and c.lower().strip() not in matched_clean
    }

    top_matched = [c.title() for c in deduplicate_phrases(sorted(matched_clean, key=len, reverse=True)[:5])]
    filtered_missing = {
        c for c in missing_clean
        if not any(h in c.split() for h in SECTION_HEADERS)
    }
    top_missing = [c.title() for c in deduplicate_phrases(sorted(filtered_missing, key=len, reverse=True))][:5]

    # Fit rating
    if score > 80:
        status = "Strong fit"
        suggestion = "You are highly aligned with this job — definitely consider applying!"
    elif score > 60:
        status = "Moderate fit"
        suggestion = "You meet many of the job’s requirements, but there may be a few areas to improve."
    else:
        status = "Weak fit"
        suggestion = "Your resume may not align closely with this job. Consider tailoring it more or applying elsewhere."

    summary = f"""
**{status}** — Match Score: {score}%

✅ **Matched concepts:** {', '.join(top_matched) if top_matched else 'N/A'}  
⚠️ **Missing concepts:**  
{''.join(f'- {item}\n' for item in top_missing) if top_missing else '- None detected'}

💡 **Recommendation:** {suggestion}
"""
    return summary

def highlight_matches(resume_text, job_text):
    concepts = list(extract_dynamic_concepts(job_text))
    # Sort longest first to avoid partial matches (e.g. "cloud infrastructure" before "cloud")
    concepts = sorted(concepts, key=len, reverse=True)

    highlighted = resume_text
    for concept in concepts:
        # Word boundary + case insensitive
        pattern = re.compile(rf'\b{re.escape(concept)}\b', re.IGNORECASE)
        highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", highlighted)

    return highlighted
