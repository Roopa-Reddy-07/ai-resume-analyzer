import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(file_path="data/job_roles.csv"):
    """Load job role requirements from CSV."""
    return pd.read_csv(file_path)


# ---------------------------------------
# Skill Normalization
# ---------------------------------------

def normalize_skill(skill):
    """
    Normalize skill names so common variants
    are treated as equivalent.
    """

    skill = skill.strip().lower()

    aliases = {
        "html5": "html",
        "css3": "css",
        "node.js": "nodejs",
        "node js": "nodejs",
        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "c plus plus": "c++",
        "cpp": "c++",
        "tensorflow": "tensorflow",
        "pytorch": "pytorch"
    }

    return aliases.get(skill, skill)


# ---------------------------------------
# Skill Coverage
# ---------------------------------------

def calculate_skill_coverage(resume_skills, required_skills):
    """
    Calculate the percentage of required skills
    found in the resume.
    """

    resume_skill_names = {
        normalize_skill(skill["skill"])
        for skill in resume_skills
    }

    required_skill_list = [
        normalize_skill(skill)
        for skill in required_skills.split(",")
        if skill.strip()
    ]

    if not required_skill_list:
        return 0.0

    matched_skills = [
        skill
        for skill in required_skill_list
        if skill in resume_skill_names
    ]

    coverage = (
        len(matched_skills) / len(required_skill_list)
    ) * 100

    return coverage


# ---------------------------------------
# TF-IDF Similarity
# ---------------------------------------

def calculate_tfidf_similarity(resume_text, job_description):
    """
    Calculate TF-IDF cosine similarity between
    resume text and job description.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity * 100


# ---------------------------------------
# Final Match Score
# ---------------------------------------

def calculate_match_score(
    skill_coverage,
    tfidf_similarity
):
    """
    Calculate final weighted match score.

    70% skill coverage
    30% TF-IDF similarity
    """

    score = (
        0.70 * skill_coverage
        + 0.30 * tfidf_similarity
    )

    return round(score, 2)


# ---------------------------------------
# Rank Job Roles
# ---------------------------------------

def rank_job_roles(
    resume_text,
    resume_skills,
    job_roles
):
    """
    Compare the resume against all job roles
    and return ranked recommendations.
    """

    results = []

    for _, role in job_roles.iterrows():

        skill_coverage = calculate_skill_coverage(
            resume_skills,
            role["required_skills"]
        )

        tfidf_similarity = calculate_tfidf_similarity(
            resume_text,
            role["job_description"]
        )

        match_score = calculate_match_score(
            skill_coverage,
            tfidf_similarity
        )

        results.append({
            "job_role": role["job_role"],
            "skill_coverage": round(
                skill_coverage, 2
            ),
            "tfidf_similarity": round(
                tfidf_similarity, 2
            ),
            "match_score": match_score
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="match_score",
        ascending=False
    ).reset_index(drop=True)

    return results_df


# ---------------------------------------
# Skill Gap Analysis
# ---------------------------------------

def analyze_skill_gap(
    resume_skills,
    job_role
):
    """
    Compare resume skills with the required skills
    for a selected job role.
    """

    resume_skill_names = {
        normalize_skill(skill["skill"])
        for skill in resume_skills
    }

    required_skills = [
        normalize_skill(skill)
        for skill in job_role["required_skills"].split(",")
        if skill.strip()
    ]

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skill_names
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skill_names
    ]

    return matched_skills, missing_skills