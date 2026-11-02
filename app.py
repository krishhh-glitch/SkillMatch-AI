import streamlit as st
from pypdf import PdfReader
from io import BytesIO
import pandas as pd

from src.skill_extractor import extract_skills
from src.ml_similarity import calculate_similarity
from src.job_classifier import predict_job_category


# Page configuration
st.set_page_config(
    page_title="SkillMatch AI",
    page_icon="🎯",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background-color: #F5F8FF;
        color: #1E293B;
    }

    [data-testid="stSidebar"] {
        background-color: #E8F0FE;
    }

    [data-testid="stSidebar"] * {
        color: #1E293B !important;
    }

    h1, h2, h3, p, label, span {
        color: #1E293B;
    }

    .stMarkdown p,
    .stMarkdown li {
        color: #334155;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1E293B !important;
    }

    .stButton > button {
        background-color: #2563EB;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: #FFFFFF;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Session storage for analysis results
if "analysis" not in st.session_state:
    st.session_state.analysis = None


# Professional Header
st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h1 style="color:#4F8BF9;">
            🎯 SkillMatch AI
        </h1>
        <h3>AI-Powered Resume & Job Matcher</h3>
        <p>
            Analyze your resume, discover skill gaps,
            and improve your career opportunities.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Sidebar Navigation
st.sidebar.title("🎯 SkillMatch AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Resume Analysis",
        "🎓 Skill Recommendations",
        "ℹ️ About Project"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "AI-powered career assistance "
    "for students and job seekers."
)


if page == "🏠 Home":
    st.markdown("""
        <div style="
            background: linear-gradient(120deg, #1D4ED8, #60A5FA);
            padding: 35px;
            border-radius: 18px;
            color: white;
            text-align: center;
        ">
            <h1 style="color:white;">🎯 Welcome to SkillMatch AI</h1>
            <h3 style="color:white;">Your AI-Powered Career Assistant</h3>
            <p>Match your skills with job opportunities and discover
            what you need to learn next.</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.subheader("✨ Explore Your Career Tools")

    col1, col2 = st.columns(2)

    with col1:
        st.info("📄 **Resume Analysis**\n\nAnalyze your resume against job descriptions.")
        st.info("🎯 **Compatibility Score**\n\nMeasure how closely your resume matches a job.")

    with col2:
        st.info("🧠 **Skill Gap Detection**\n\nIdentify skills you are missing.")
        st.info("🎓 **Skill Recommendations**\n\nDiscover skills to improve your career prospects.")

    st.write("")
    st.success("👈 Select Resume Analysis from the sidebar to get started!")


# RESUME ANALYSIS PAGE
elif page == "📊 Resume Analysis":

    st.header("📊 Resume Analysis")

    st.write(
        "Upload your resume and paste a job description "
        "to calculate your compatibility."
    )

    resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the job requirements..."
    )

    if st.button("Analyze My Resume"):

        if resume is None:
            st.warning("Please upload your resume.")

        elif not job_description.strip():
            st.warning("Please enter a job description.")

        else:

            try:
                pdf_reader = PdfReader(
                    BytesIO(resume.getvalue())
                )

                resume_text = ""

                for pdf_page in pdf_reader.pages:
                    extracted_text = (
                        pdf_page.extract_text() or ""
                    )
                    resume_text += extracted_text + "\n"

                if not resume_text.strip():

                    st.warning(
                        "No readable text found. "
                        "This PDF may contain scanned images."
                    )

                else:

                    # Extract skills
                    resume_skills = extract_skills(resume_text)

                    job_skills = extract_skills(job_description)

                    matching_skills = [
                        skill for skill in job_skills
                        if skill in resume_skills
                    ]

                    missing_skills = [
                        skill for skill in job_skills
                        if skill not in resume_skills
                    ]

                    # ML Similarity
                    compatibility = calculate_similarity(
                        resume_text,
                        job_description
                    )

                    # Job Classification
                    predicted_category = predict_job_category(
                        job_description
                    )

                    # Save results
                    st.session_state.analysis = {
                        "resume_text": resume_text,
                        "resume_skills": resume_skills,
                        "job_skills": job_skills,
                        "matching_skills": matching_skills,
                        "missing_skills": missing_skills,
                        "compatibility": compatibility,
                        "predicted_category": predicted_category
                    }

                    st.success(
                        "Resume analyzed successfully!"
                    )

            except Exception as error:
                st.error(f"Unable to analyze resume: {error}")


    # Display saved analysis results
    if st.session_state.analysis is not None:

        result = st.session_state.analysis

        st.divider()

        st.subheader("📊 Your Resume Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🎯 Resume Match",
                f"{result['compatibility']:.2f}%"
            )

        with col2:
            st.metric(
                "✅ Matching Skills",
                len(result["matching_skills"])
            )

        with col3:
            st.metric(
                "❌ Missing Skills",
                len(result["missing_skills"])
            )

        st.progress(max(0, min(100, int(result["compatibility"]))))


        st.subheader("💼 Predicted Job Category")

        st.markdown(f"""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #2563EB;
            margin-bottom: 20px;
        ">
            <p style="color: #64748B; margin-bottom: 5px;">
                Your best-matching job category
            </p>
            <h2 style="color: #1D4ED8; margin: 0;">
                {result['predicted_category']}
            </h2>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🧠 Skill Analysis")

        st.write(
            "Skills found in your resume:",
            result["resume_skills"]
        )

        st.write(
            "Skills required by the job:",
            result["job_skills"]
        )

        st.subheader("🧠 Detailed Skill Analysis")

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:
            st.markdown("### ✅ Matching Skills")
            if result["matching_skills"]:
                for skill in result["matching_skills"]:
                    st.success(f"✓ {skill}")
            else:
                st.info("No matching skills found.")

        with skill_col2:
            st.markdown("### 📌 Skills to Improve")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.warning(f"＋ {skill}")
            else:
                st.success("You have all the required skills!")

        # Skills Chart
        st.subheader("📊 Skills Overview")

        chart_data = pd.DataFrame({
            "Category": [
                "Matching Skills",
                "Missing Skills"
            ],
            "Count": [
                len(result["matching_skills"]),
                len(result["missing_skills"])
            ]
        })

        st.bar_chart(
            chart_data,
            x="Category",
            y="Count"
        )

        # Extracted Resume Text
        with st.expander("📃 View Extracted Resume Text"):

            st.text_area(
                "Resume Content",
                value=result["resume_text"],
                height=300
            )


# SKILL RECOMMENDATIONS PAGE
elif page == "🎓 Skill Recommendations":
    st.header("🎓 Your Personalized Skill Roadmap")

    if st.session_state.analysis is None:
        st.info(
            "Please analyze your resume first "
            "to receive personalized recommendations."
        )
    else:
        missing_skills = st.session_state.analysis["missing_skills"]

        if missing_skills:
            st.write(
                "Focus on developing these skills to improve "
                "your match with the selected job."
            )

            st.subheader("📚 Skills to Learn")

            for index, skill in enumerate(missing_skills, start=1):
                with st.container(border=True):
                    st.markdown(f"**{index}. {skill}**")
                    st.write(
                        f"Add {skill} to your learning roadmap "
                        "and practice it through projects."
                    )

            st.info(
                "💡 Tip: Build a small practical project "
                "for each skill you learn."
            )

        else:
            st.success(
                "🎉 Excellent! Your resume includes all "
                "the skills detected in this job description."
            )


# ABOUT PAGE
elif page == "ℹ️ About Project":
    st.header("ℹ️ About SkillMatch AI")

    st.markdown("""
    ### 🎯 Project Overview

    SkillMatch AI is an AI-powered resume and job matching
    application designed to help students and job seekers
    identify skill gaps and explore career opportunities.

    ### 🚀 Key Features

    - Resume text extraction from PDF files
    - Resume and job description similarity scoring
    - Automatic job category prediction
    - Matching and missing skill identification
    - Personalized skill recommendations
    - Interactive analysis dashboard

    ### 🛠️ Technologies Used
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("🐍 Python")
        st.info("🎨 Streamlit")
        st.info("🤖 Scikit-learn")
        st.info("📊 Pandas")

    with col2:
        st.info("🧠 Natural Language Processing")
        st.info("📈 TF-IDF")
        st.info("🎯 Cosine Similarity")
        st.info("🔍 Logistic Regression")

    st.divider()

    st.subheader("🌟 Project Objective")
    st.write(
        "To make job preparation smarter by helping candidates "
        "understand their strengths, identify skill gaps, "
        "and improve their employability."
    )


# Footer
st.divider()

st.caption(
    "SkillMatch AI | Built with Python and Streamlit"
)