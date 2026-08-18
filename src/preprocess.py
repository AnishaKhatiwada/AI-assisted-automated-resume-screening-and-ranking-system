import re

from extract_text import extract_text_from_pdf


def clean_text(text):
    """
    Clean extracted resume text while preserving
    meaningful information for semantic matching.
    """

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Normalize different dash characters
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Remove unwanted non-printable characters
    text = re.sub(r"[^\x20-\x7E]", " ", text)

    # Remove repeated whitespace again
    text = re.sub(r"\s+", " ", text)

    return text.strip()


if __name__ == "__main__":

    file_path = "data/resumes/test_resume.pdf"

    raw_text = extract_text_from_pdf(file_path)

    cleaned_text = clean_text(raw_text)

    print("Resume text extracted and cleaned successfully!")
    print("-----------------------------------------------")
    print(cleaned_text)