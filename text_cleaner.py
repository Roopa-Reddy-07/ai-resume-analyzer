import re


def clean_resume_text(text):
    """
    Clean and normalize extracted resume text
    while preserving important technical terms.
    """

    # Convert to lowercase
    text = text.lower()

    # Normalize common technical terms
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")
    text = text.replace("node.js", "nodejs")
    text = text.replace("react.js", "react")

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Replace unwanted characters with spaces
    # Keep letters, numbers, +, #, -, and .
    text = re.sub(r"[^a-zA-Z0-9+#.\-\s]", " ", text)

    # Remove standalone punctuation
    text = re.sub(r"(?<!\w)[.#]+(?!\w)", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()