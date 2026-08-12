from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import load_skill_dictionary, extract_skills


file_path = "sample_resumes/sample_resume.pdf"


# Extract resume text
with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


# Clean resume text
cleaned_text = clean_resume_text(extracted_text)


# Load skill dictionary
skill_dictionary = load_skill_dictionary()


# Extract skills
skills = extract_skills(cleaned_text, skill_dictionary)


print("\n----- SKILLS DETECTED -----\n")

for skill in skills:
    print(
        f"{skill['display_name']} "
        f"({skill['category']})"
    )