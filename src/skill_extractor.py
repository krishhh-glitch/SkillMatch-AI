import re

# Skills our application can recognize
SKILLS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "SQL",
    "MySQL",
    "MongoDB",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Git",
    "GitHub",
    "Linux",
    "AWS",
    "Docker",
    "Flask",
    "Django",
    "Streamlit",
    "REST API"
]


def extract_skills(text):

    found_skills = []

    # Convert text to lowercase
    text = text.lower()

    # Check every skill
    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills