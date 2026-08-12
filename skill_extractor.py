import pandas as pd
import re


def load_skill_dictionary(file_path="data/skill_dictionary.csv"):
    """Load the controlled skill dictionary."""

    return pd.read_csv(file_path)


def extract_skills(text, skill_dictionary):
    """
    Extract skills from cleaned resume text.

    Returns:
        A list of dictionaries containing skill,
        display name, and category.
    """

    found_skills = []

    for _, row in skill_dictionary.iterrows():

        skill = str(row["skill"]).lower()

        # Create a regex pattern for whole-word matching
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text.lower()):
            found_skills.append({
                "skill": skill,
                "display_name": row["display_name"],
                "category": row["category"]
            })

    return found_skills