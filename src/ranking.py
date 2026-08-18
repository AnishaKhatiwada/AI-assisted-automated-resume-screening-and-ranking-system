import os

from similarity import analyze_resume


def rank_resumes(
    resume_folder,
    job_description_path
):
    """
    Analyze all PDF resumes in a folder
    and rank them according to overall score.
    """

    results = []

    for filename in os.listdir(
        resume_folder
    ):

        if not filename.lower().endswith(
            ".pdf"
        ):
            continue

        resume_path = os.path.join(
            resume_folder,
            filename
        )

        try:

            analysis = analyze_resume(
                resume_path,
                job_description_path
            )

            results.append({

                "resume":
                    filename,

                "semantic_similarity":
                    analysis[
                        "semantic_similarity"
                    ],

                "skill_match":
                    analysis[
                        "skill_match"
                    ],

                "overall_score":
                    analysis[
                        "overall_score"
                    ],

                "matched_skills":
                    analysis[
                        "matched_skills"
                    ],

                "missing_skills":
                    analysis[
                        "missing_skills"
                    ]
            })

        except Exception as error:

            print(
                f"Error processing "
                f"{filename}: {error}"
            )

    # Sort by overall score
    results.sort(
        key=lambda x:
        x["overall_score"],
        reverse=True
    )

    # Add ranking position
    for position, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = position

    return results


if __name__ == "__main__":

    resume_folder = (
        "data/resumes"
    )

    job_description_path = (
        "data/job_description.txt"
    )

    ranked_results = rank_resumes(
        resume_folder,
        job_description_path
    )

    print("\n===================================")
    print("       CANDIDATE RANKING")
    print("===================================")

    if not ranked_results:

        print("No PDF resumes found.")

    else:

        for result in ranked_results:

            print(
                f"\nRank {result['rank']}: "
                f"{result['resume']}"
            )

            print(
                "Semantic similarity:",
                result[
                    "semantic_similarity"
                ],
                "%"
            )

            print(
                "Skill match:",
                result["skill_match"],
                "%"
            )

            print(
                "Overall score:",
                result["overall_score"],
                "%"
            )

            print(
                "Matched skills:",
                ", ".join(
                    result[
                        "matched_skills"
                    ]
                )
            )

            if result[
                "missing_skills"
            ]:

                print(
                    "Missing skills:",
                    ", ".join(
                        result[
                            "missing_skills"
                        ]
                    )
                )

            else:

                print(
                    "Missing skills: None"
                )

    print("\n===================================")