from sentence_transformers import SentenceTransformer, util
import spacy

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

def extract_concepts(text):
    """
    Extracts noun phrases (key concepts) from text using spaCy.
    """
    doc = nlp(text)
    return set(chunk.text.lower().strip() for chunk in doc.noun_chunks if len(chunk.text) > 3)

def generate_summary(resume_text, job_text, score):
    """
    Generates a natural-language summary of the resume-job match.
    """
    resume_concepts = extract_concepts(resume_text)
    job_concepts = extract_concepts(job_text)

    matched = resume_concepts.intersection(job_concepts)
    missing = job_concepts.difference(resume_concepts)

    top_matched = list(matched)[:5]
    top_missing = list(missing)[:5]

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
⚠️ **Missing concepts:** {', '.join(top_missing) if top_missing else 'None detected'}  

💡 **Recommendation:** {suggestion}
    """

    return summary
