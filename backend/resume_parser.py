import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file_path):
    """
    Extract raw text from a PDF file.

    Args:
        file_path (str): Path to the uploaded resume PDF.

    Returns:
        str: Concatenated text from all pages.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_resume_text(text):
    """
    Parse resume text using spaCy NLP to extract basic info.

    Args:
        text (str): Raw resume text.

    Returns:
        dict: Parsed info including name, skills, education.
    """
    doc = nlp(text)

    name = None
    skills = []
    education = []
    experience = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "ORG":
            education.append(ent.text)

    # Simple skill matching using a predefined list
    common_skills = [
        "python", "java", "c++", "react", "docker", "sql",
        "tensorflow", "pandas", "flask", "ros", "gazebo",
        "javascript", "node", "mysql", "sklearn", "matplotlib"
    ]

    for skill in common_skills:
        if skill.lower() in text.lower():
            skills.append(skill.lower())

    return {
        "name": name,
        "skills": list(set(skills)),
        "education": list(set(education))
    }

def parse_resume(file_path):
    """
    End-to-end resume parsing pipeline.

    Args:
        file_path (str): PDF file path.

    Returns:
        dict: Parsed resume information.
    """
    text = extract_text_from_pdf(file_path)
    return parse_resume_text(text)


# Test this file directly
if __name__ == "__main__":
    sample_file = "data/sample_resumes/sample_resume.pdf"
    parsed = parse_resume(sample_file)
    print(parsed)
