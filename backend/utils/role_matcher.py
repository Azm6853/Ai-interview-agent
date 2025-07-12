# backend/utils/role_matcher.py

ROLE_TEMPLATES = {
    "Software Engineer": ["python", "c++", "react", "docker", "flask", "java", "git"],
    "Data Scientist": ["pandas", "tensorflow", "sklearn", "numpy", "matplotlib", "nlp"],
    "Product Manager": ["agile", "roadmap", "stakeholders", "ux", "prioritization"],
    "Robotics Engineer": ["ros", "gazebo", "navigation", "path planning", "robotics"],
    "Full Stack Developer": ["javascript", "react", "node", "mysql", "api", "docker"]
}


def match_role(skills):
    """
    Match the user's skills to a predefined role based on keyword overlap.

    Args:
        skills (list of str): A list of skills extracted from the resume.

    Returns:
        dict: {
            "matched_role": str,
            "score": int
        }
    """
    scores = {}
    for role, keywords in ROLE_TEMPLATES.items():
        score = len(set(skill.lower() for skill in skills) & set(keywords))
        scores[role] = score

    matched_role = max(scores, key=scores.get)
    return {
        "matched_role": matched_role,
        "score": scores[matched_role]
    }


# Example usage
if __name__ == "__main__":
    sample_skills = ["Python", "Docker", "React", "SQL"]
    result = match_role(sample_skills)
    print("Best matched role:", result)

