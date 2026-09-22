import streamlit as st
import matplotlib.pyplot as plt
from utils import clean_text, compute_similarity, keyword_gap, generate_suggestions

st.set_page_config(page_title="Resume Optimizer AI", layout="wide")

st.title("📄 Resume Optimizer AI")

# Input section
col1, col2 = st.columns(2)

with col1:
    resume = st.text_area("📄 Paste Your Resume", height=200)

with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=200)

# Analyze button
if st.button("Analyze"):
    if resume and job_desc:

        resume_clean = clean_text(resume)
        job_clean = clean_text(job_desc)

        score = compute_similarity(resume_clean, job_clean)
        missing, matched = keyword_gap(resume_clean, job_clean)
        suggestions = generate_suggestions(score, missing)

        # Score section
        st.subheader("📊 Match Score")
        st.progress(int(score))
        st.success(f"{score}% Match")

        # Columns for results
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✅ Matched Skills")
            st.write(matched)

        with col4:
            st.subheader("❌ Missing Skills")
            st.write(missing)

        # Chart (VERY IMPRESSIVE)
        st.subheader("📈 Skill Comparison")

        labels = ["Matched", "Missing"]
        values = [len(matched), len(missing)]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Count")
        ax.set_title("Skill Match Overview")

        st.pyplot(fig)

        # Suggestions
        st.subheader("💡 Suggestions")
        for s in suggestions:
            st.write("- " + s)

    else:
        st.warning("Please enter both resume and job description.")