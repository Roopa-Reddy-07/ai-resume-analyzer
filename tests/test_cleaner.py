from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text


file_path = "sample_resumes/sample_resume.pdf"

with open(file_path, "rb") as file:
    extracted_text = extract_resume_text(file)


cleaned_text = clean_resume_text(extracted_text)

print("\n----- CLEANED RESUME TEXT -----\n")
print(cleaned_text)