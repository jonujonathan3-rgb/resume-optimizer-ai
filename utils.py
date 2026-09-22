import re
import nltk
import spacy
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def load_skills():
    with open("skills.txt", "r") as f:
        skills = [line.strip().lower() for line in f.readlines()]
    return skills


def extract_keywords(text):
    skills = load_skills()
    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
def compute_similarity(resume, job_desc):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume, job_desc])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(score * 100, 2)
def keyword_gap(resume, job_desc):
    resume_words = set(extract_keywords(resume))
    job_words = set(extract_keywords(job_desc))

    missing = job_words - resume_words
    matched = job_words & resume_words

    return list(missing), list(matched)
def generate_suggestions(score, missing_keywords):
    suggestions = []

    if score < 50:
        suggestions.append("Your resume is not well aligned with the job. Try tailoring it more.")

    if missing_keywords:
        suggestions.append("Add these missing skills: " + ", ".join(missing_keywords[:5]))

    suggestions.append("Use action verbs like 'developed', 'built', 'led'.")
    suggestions.append("Add measurable achievements (e.g., improved performance by 20%).")

    return suggestions