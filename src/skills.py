import re


SKILL_VARIATIONS = {

    "Java": [
        "java"
    ],

    "Spring Boot": [
        "spring boot",
        "springboot"
    ],

    "REST APIs": [
        "rest api",
        "rest apis",
        "restapi",
        "restapis"
    ],

    "SQL": [
        "sql",
        "structured query language"
    ],

    "MySQL": [
        "mysql"
    ],

    "Microsoft SQL Server": [
        "microsoft sql server",
        "microsoftsqlserver"
    ],

    "MongoDB": [
        "mongodb"
    ],

    "Angular": [
        "angular"
    ],

    "TypeScript": [
        "typescript"
    ],

    "Python": [
        "python"
    ],

    "Git": [
        "git",
        "gitlab"
    ],

    "Jenkins": [
        "jenkins"
    ],

    "Docker": [
        "docker"
    ],

    "Postman": [
        "postman"
    ],

    "Agile": [
        "agile"
    ],

    "JavaScript": [
        "javascript"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "scss"
    ]
}


def normalize_text(text):
    """
    Normalize text for skill matching.
    Handles common PDF extraction spacing problems.
    """

    text = text.lower()

    # Handle common PDF spacing variations
    text = text.replace("springboot", "spring boot")
    text = text.replace("restapis", "rest apis")
    text = text.replace("restapi", "rest api")
    text = text.replace("microsoftsqlserver", "microsoft sql server")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text


def contains_skill(text, skill):
    """
    Check whether a skill is present in the text.
    """

    text = normalize_text(text)

    variations = SKILL_VARIATIONS.get(
        skill,
        [skill.lower()]
    )

    for variation in variations:

        # Use word boundaries for short/common terms
        pattern = r"(?<!\w)" + re.escape(variation) + r"(?!\w)"

        if re.search(pattern, text):
            return True

    return False


def extract_skills(text):
    """
    Extract recognized technical skills.
    """

    found_skills = []

    for skill in SKILL_VARIATIONS:

        if contains_skill(text, skill):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text, job_description):
    """
    Compare resume skills with job requirements.
    """

    resume_skills = extract_skills(resume_text)

    required_skills = extract_skills(job_description)

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills
    ]

    if required_skills:

        skill_match_percentage = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        skill_match_percentage = 0

    return {

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_match_percentage":
            round(skill_match_percentage, 2)
    }