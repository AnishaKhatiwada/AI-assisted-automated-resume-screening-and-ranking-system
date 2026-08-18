import os
import sys
import csv
import re
import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATH SETUP
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data"
)

RESUME_FOLDER = os.path.join(
    DATA_PATH,
    "resumes"
)

CANDIDATES_FILE = os.path.join(
    DATA_PATH,
    "candidates.csv"
)

JOB_DESCRIPTION_FILE = os.path.join(
    DATA_PATH,
    "job_description.txt"
)


# Add src folder to Python path
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# Import our AI analysis pipeline
from similarity import analyze_resume


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

os.makedirs(
    RESUME_FOLDER,
    exist_ok=True
)

os.makedirs(
    DATA_PATH,
    exist_ok=True
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Scanner",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# FUNCTIONS
# ============================================================

def safe_filename(filename):
    """
    Make uploaded filename safe for saving.
    """

    filename = os.path.basename(filename)

    filename = re.sub(
        r"[^A-Za-z0-9_.-]",
        "_",
        filename
    )

    return filename


def get_unique_filename(filename):
    """
    Prevent overwriting an existing resume.
    """

    filename = safe_filename(filename)

    base, extension = os.path.splitext(
        filename
    )

    candidate_path = os.path.join(
        RESUME_FOLDER,
        filename
    )

    counter = 1

    while os.path.exists(candidate_path):

        new_filename = (
            f"{base}_{counter}{extension}"
        )

        candidate_path = os.path.join(
            RESUME_FOLDER,
            new_filename
        )

        counter += 1

    return os.path.basename(
        candidate_path
    )


def save_uploaded_resume(uploaded_file):
    """
    Save uploaded PDF permanently inside
    data/resumes/.
    """

    filename = get_unique_filename(
        uploaded_file.name
    )

    file_path = os.path.join(
        RESUME_FOLDER,
        filename
    )

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return file_path, filename


def load_candidates():
    """
    Load candidate records from candidates.csv.
    """

    if not os.path.exists(
        CANDIDATES_FILE
    ):

        return pd.DataFrame(
            columns=[
                "rank",
                "candidate",
                "resume",
                "semantic_similarity",
                "skill_match",
                "overall_score",
                "matched_skills",
                "missing_skills"
            ]
        )

    try:

        df = pd.read_csv(
            CANDIDATES_FILE
        )

        return df

    except Exception:

        return pd.DataFrame(
            columns=[
                "rank",
                "candidate",
                "resume",
                "semantic_similarity",
                "skill_match",
                "overall_score",
                "matched_skills",
                "missing_skills"
            ]
        )


def save_candidate(
    candidate_name,
    resume_filename,
    results
):
    """
    Add candidate analysis result to CSV.
    """

    df = load_candidates()

    new_candidate = pd.DataFrame([
        {
            "rank": 0,

            "candidate":
                candidate_name,

            "resume":
                resume_filename,

            "semantic_similarity":
                results[
                    "semantic_similarity"
                ],

            "skill_match":
                results[
                    "skill_match"
                ],

            "overall_score":
                results[
                    "overall_score"
                ],

            "matched_skills":
                "; ".join(
                    results[
                        "matched_skills"
                    ]
                ),

            "missing_skills":
                "; ".join(
                    results[
                        "missing_skills"
                    ]
                )
                if results[
                    "missing_skills"
                ]
                else "None"
        }
    ])

    # Add new candidate
    df = pd.concat(
        [
            df,
            new_candidate
        ],
        ignore_index=True
    )

    # Sort by overall score
    df = df.sort_values(
        by="overall_score",
        ascending=False
    )

    # Reset ranking
    df["rank"] = range(
        1,
        len(df) + 1
    )

    # Save updated CSV
    df.to_csv(
        CANDIDATES_FILE,
        index=False
    )

    return df


def rank_candidates():
    """
    Read candidates.csv and update ranking.
    """

    df = load_candidates()

    if df.empty:
        return df

    # Ensure score is numeric
    df["overall_score"] = pd.to_numeric(
        df["overall_score"],
        errors="coerce"
    )

    # Sort highest score first
    df = df.sort_values(
        by="overall_score",
        ascending=False
    ).reset_index(
        drop=True
    )

    # Assign rank
    df["rank"] = range(
        1,
        len(df) + 1
    )

    # Save updated ranking
    df.to_csv(
        CANDIDATES_FILE,
        index=False
    )

    return df


def load_job_description():
    """
    Load the job description from
    data/job_description.txt.
    """

    if not os.path.exists(
        JOB_DESCRIPTION_FILE
    ):

        return ""

    with open(
        JOB_DESCRIPTION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# HEADER
# ============================================================

st.title(
    "📄 AI Resume Scanner"
)

st.subheader(
    "Intelligent Candidate Screening System"
)

st.write(
    """
    An AI-assisted resume screening system that analyzes
    candidate resumes against job requirements using
    transformer-based semantic similarity and technical
    skill matching.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ System Information"
    )

    st.write(
        """
        **AI Model**

        Sentence Transformer  
        `all-MiniLM-L6-v2`

        **Embedding Size**

        384 dimensions

        **Scoring**

        Semantic Similarity: 70%

        Skill Match: 30%

        **Storage**

        Candidate resumes → `data/resumes/`

        Candidate results → `data/candidates.csv`
        """
    )


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.header(
    "1️⃣ Job Requirement"
)

job_description = load_job_description()

job_description = st.text_area(
    "Enter or edit the job requirements:",
    value=job_description,
    height=250
)


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header(
    "2️⃣ Upload Candidate Resume"
)

uploaded_file = st.file_uploader(
    "Upload a candidate resume in PDF format",
    type=["pdf"]
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze & Rank Candidate",
    type="primary"
):

    if uploaded_file is None:

        st.warning(
            "Please upload a PDF resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please provide a job description."
        )

    else:

        try:

            # ------------------------------------------------
            # Save uploaded resume permanently
            # ------------------------------------------------

            with st.spinner(
                "Saving candidate resume..."
            ):

                resume_path, resume_filename = (
                    save_uploaded_resume(
                        uploaded_file
                    )
                )

            # ------------------------------------------------
            # Save current JD
            # ------------------------------------------------

            with open(
                JOB_DESCRIPTION_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    job_description
                )

            # ------------------------------------------------
            # Analyze resume
            # ------------------------------------------------

            with st.spinner(
                "AI is analyzing the resume..."
            ):

                results = analyze_resume(
                    resume_path,
                    JOB_DESCRIPTION_FILE
                )

            # ------------------------------------------------
            # Candidate name
            # ------------------------------------------------

            candidate_name = os.path.splitext(
                resume_filename
            )[0]

            # ------------------------------------------------
            # Save candidate result
            # ------------------------------------------------

            ranking_df = save_candidate(
                candidate_name,
                resume_filename,
                results
            )

            # ------------------------------------------------
            # Success
            # ------------------------------------------------

            st.success(
                "Resume analyzed and candidate added "
                "to the ranking!"
            )

            # ------------------------------------------------
            # Candidate analysis
            # ------------------------------------------------

            st.header(
                "3️⃣ Candidate Analysis"
            )

            st.write(
                f"**Candidate:** {candidate_name}"
            )

            st.write(
                f"**Resume:** {resume_filename}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Semantic Similarity",
                    f"{results['semantic_similarity']:.2f}%"
                )

            with col2:

                st.metric(
                    "Skill Match",
                    f"{results['skill_match']:.2f}%"
                )

            with col3:

                st.metric(
                    "Overall Score",
                    f"{results['overall_score']:.2f}%"
                )

            # ------------------------------------------------
            # Skill analysis
            # ------------------------------------------------

            st.header(
                "4️⃣ Skill Analysis"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Matched Skills"
                )

                if results[
                    "matched_skills"
                ]:

                    for skill in results[
                        "matched_skills"
                    ]:

                        st.write(
                            f"✓ {skill}"
                        )

                else:

                    st.write(
                        "No required skills matched."
                    )

            with col2:

                st.subheader(
                    "❌ Missing Skills"
                )

                if results[
                    "missing_skills"
                ]:

                    for skill in results[
                        "missing_skills"
                    ]:

                        st.write(
                            f"✗ {skill}"
                        )

                else:

                    st.write(
                        "None"
                    )

            # ------------------------------------------------
            # Candidate's detected skills
            # ------------------------------------------------

            st.header(
                "5️⃣ Detected Resume Skills"
            )

            if results[
                "resume_skills"
            ]:

                st.write(
                    ", ".join(
                        results[
                            "resume_skills"
                        ]
                    )
                )

            else:

                st.write(
                    "No recognized skills detected."
                )

            # ------------------------------------------------
            # Candidate ranking
            # ------------------------------------------------

            st.header(
                "🏆 6️⃣ Candidate Ranking"
            )

            ranking_df = rank_candidates()

            display_df = ranking_df[
                [
                    "rank",
                    "candidate",
                    "semantic_similarity",
                    "skill_match",
                    "overall_score"
                ]
            ].copy()

            display_df.columns = [
                "Rank",
                "Candidate",
                "Semantic Similarity (%)",
                "Skill Match (%)",
                "Overall Score (%)"
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # Top candidate
            # ------------------------------------------------

            if not ranking_df.empty:

                top_candidate = (
                    ranking_df.iloc[0]
                )

                st.info(
                    f"🏆 Current Top Candidate: "
                    f"**{top_candidate['candidate']}** "
                    f"with an overall score of "
                    f"**{float(top_candidate['overall_score']):.2f}%**"
                )

        except Exception as error:

            st.error(
                "An error occurred while processing "
                "the resume."
            )

            st.exception(
                error
            )


# ============================================================
# EXISTING CANDIDATES / RANKING
# ============================================================

st.divider()

st.header(
    "📊 Current Candidate Ranking"
)

existing_candidates = rank_candidates()

if existing_candidates.empty:

    st.info(
        "No candidates have been analyzed yet. "
        "Upload a resume above to create the first candidate."
    )

else:

    display_existing = existing_candidates[
        [
            "rank",
            "candidate",
            "semantic_similarity",
            "skill_match",
            "overall_score"
        ]
    ].copy()

    display_existing.columns = [
        "Rank",
        "Candidate",
        "Semantic Similarity (%)",
        "Skill Match (%)",
        "Overall Score (%)"
    ]

    st.dataframe(
        display_existing,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Resume Scanner | Transformer-based semantic "
    "matching and skill-aware candidate ranking"
)