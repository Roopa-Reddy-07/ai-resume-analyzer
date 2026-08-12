from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import (
    load_skill_dictionary,
    extract_skills
)
from job_matcher import (
    load_job_roles,
    rank_job_roles
)


# --------------------------------
# 1. Load resume
# --------------------------------

file_path = "sample_resumes/sample_resume.pdf"

with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


# --------------------------------
# 2. Clean resume
# --------------------------------

cleaned_text = clean_resume_text(
    extracted_text
)


# --------------------------------
# 3. Extract skills
# --------------------------------

skill_dictionary = load_skill_dictionary()

resume_skills = extract_skills(
    cleaned_text,
    skill_dictionary
)


# --------------------------------
# 4. Load job roles
# --------------------------------

job_roles = load_job_roles()


# --------------------------------
# 5. Rank roles
# --------------------------------

results = rank_job_roles(
    cleaned_text,
    resume_skills,
    job_roles
)


# --------------------------------
# 6. Display results
# --------------------------------

print("\n----- JOB ROLE RECOMMENDATIONS -----\n")

print(
    results.to_string(index=False)
)

print("\n----- TOP 3 ROLES -----\n")

for index, row in results.head(3).iterrows():

    print(
        f"{index + 1}. "
        f"{row['job_role']} - "
        f"{row['match_score']}%"
    )