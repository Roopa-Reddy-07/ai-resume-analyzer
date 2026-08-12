from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import (
    load_skill_dictionary,
    extract_skills
)
from job_matcher import (
    load_job_roles,
    analyze_skill_gap
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
# 5. Select target role
# --------------------------------

target_role = job_roles[
    job_roles["job_role"] == "Machine Learning Engineer"
].iloc[0]


# --------------------------------
# 6. Analyze skill gap
# --------------------------------

matched_skills, missing_skills = analyze_skill_gap(
    resume_skills,
    target_role
)


# --------------------------------
# 7. Display results
# --------------------------------

print("\n----- TARGET ROLE -----\n")
print(target_role["job_role"])


print("\n----- SKILLS FOUND -----\n")

for skill in matched_skills:
    print("✓", skill)


print("\n----- MISSING SKILLS -----\n")

for skill in missing_skills:
    print("✗", skill)