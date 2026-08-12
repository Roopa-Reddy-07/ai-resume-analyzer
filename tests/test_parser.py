from resume_parser import extract_resume_text


file_path = "sample_resumes/sample_resume.pdf"

with open(file_path, "rb") as file:
    text = extract_resume_text(file)

print("\n----- EXTRACTED RESUME TEXT -----\n")
print(text)