# role_matcher.py

def match_role(skills: list) -> dict:
    """
    Matches a candidate's skills to a likely job role.
    
    Args:
        skills (list): A list of extracted skills from resume.

    Returns:
        dict: Matched role and confidence.
    """
    role_keywords = {
        "Data Scientist": ["python", "pandas", "numpy", "sklearn", "tensorflow"],
        "Frontend Developer": ["javascript", "react", "html", "css"],
        "Backend Developer": ["python", "flask", "django", "sql"],
        "DevOps Engineer": ["docker", "kubernetes", "ci/cd", "aws"],
        "Robotics Engineer": ["ros", "gazebo", "c++"],
    }

    role_scores = {}
    for role, keywords in role_keywords.items():
        match_count = len(set(skills).intersection(set(keywords)))
        if match_count > 0:
            role_scores[role] = match_count

    if not role_scores:
        return {"matched_role": "General Engineer", "confidence": 0}

    matched_role = max(role_scores, key=role_scores.get)
    confidence = role_scores[matched_role] / len(role_keywords[matched_role])

    return {
        "matched_role": matched_role,
        "confidence": round(confidence, 2)
    }


# Test this file
if __name__ == "__main__":
    test_skills = ["python", "docker", "sql"]
    result = match_role(test_skills)
    print(result)
