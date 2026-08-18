from sklearn.metrics.pairwise import cosine_similarity

from embeddings import generate_embedding
from extract_text import extract_text_from_pdf
from preprocess import clean_text
from skills import compare_skills


def calculate_similarity(
    resume_embedding,
    job_embedding
):
    """
    Calculate cosine similarity between
    resume and job description embeddings.
    """

    similarity = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    return similarity


def similarity_to_percentage(similarity):
    """
    Convert similarity score to percentage.
    """

    return round(
        similarity * 100,
        2
    )


def calculate_overall_score(
    semantic_score,
    skill_score
):
    """
    Calculate overall candidate score.

    Semantic similarity = 70%
    Skill matching = 30%
    """

    overall_score = (
        0.70 * semantic_score
        +
        0.30 * skill_score
    )

    return round(
        overall_score,
        2
    )


def load_job_description(
    job_description_path
):
    """
    Load job description from text file.
    """

    with open(
        job_description_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def analyze_resume(
    resume_path,
    job_description_path
):
    """
    Complete resume analysis pipeline.

    Steps:
    1. Extract PDF text
    2. Preprocess text
    3. Generate embeddings
    4. Calculate semantic similarity
    5. Extract and compare skills
    6. Calculate overall score
    """

    # ---------------------------------------------
    # Extract resume
    # ---------------------------------------------

    raw_resume = extract_text_from_pdf(
        resume_path
    )

    # ---------------------------------------------
    # Preprocess resume
    # ---------------------------------------------

    resume_text = clean_text(
        raw_resume
    )

    # ---------------------------------------------
    # Load job description
    # ---------------------------------------------

    job_description = load_job_description(
        job_description_path
    )

    # ---------------------------------------------
    # Generate embeddings
    # ---------------------------------------------

    resume_embedding = generate_embedding(
        resume_text
    )

    job_embedding = generate_embedding(
        job_description
    )

    # ---------------------------------------------
    # Semantic similarity
    # ---------------------------------------------

    similarity_score = calculate_similarity(
        resume_embedding,
        job_embedding
    )

    semantic_percentage = (
        similarity_to_percentage(
            similarity_score
        )
    )

    # ---------------------------------------------
    # Skill matching
    # ---------------------------------------------

    skill_results = compare_skills(
        resume_text,
        job_description
    )

    skill_percentage = (
        skill_results[
            "skill_match_percentage"
        ]
    )

    # ---------------------------------------------
    # Overall score
    # ---------------------------------------------

    overall_score = calculate_overall_score(
        semantic_percentage,
        skill_percentage
    )

    return {

        "semantic_similarity":
            semantic_percentage,

        "skill_match":
            skill_percentage,

        "overall_score":
            overall_score,

        "resume_skills":
            skill_results[
                "resume_skills"
            ],

        "required_skills":
            skill_results[
                "required_skills"
            ],

        "matched_skills":
            skill_results[
                "matched_skills"
            ],

        "missing_skills":
            skill_results[
                "missing_skills"
            ]
    }


if __name__ == "__main__":

    resume_path = (
        "data/resumes/test_resume.pdf"
    )

    job_description_path = (
        "data/job_description.txt"
    )

    results = analyze_resume(
        resume_path,
        job_description_path
    )

    print("\n===================================")
    print("       RESUME MATCH RESULT")
    print("===================================")

    print(
        "Semantic similarity:",
        results["semantic_similarity"],
        "%"
    )

    print(
        "Skill match:",
        results["skill_match"],
        "%"
    )

    print(
        "Overall candidate score:",
        results["overall_score"],
        "%"
    )

    print("\n-----------------------------------")
    print("Required Skills")
    print("-----------------------------------")

    for skill in results["required_skills"]:
        print("-", skill)

    print("\n-----------------------------------")
    print("Matched Skills")
    print("-----------------------------------")

    for skill in results["matched_skills"]:
        print("✓", skill)

    print("\n-----------------------------------")
    print("Missing Skills")
    print("-----------------------------------")

    if results["missing_skills"]:

        for skill in results["missing_skills"]:
            print("✗", skill)

    else:

        print("None")

    print("===================================")