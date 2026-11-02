from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Sample training data
job_descriptions = [
    "Python pandas numpy data analysis statistics",
    "SQL database data visualization analyst",
    "React HTML CSS JavaScript frontend",
    "Node.js Django Flask web development",
    "TensorFlow PyTorch deep learning neural networks",
    "Machine learning NLP artificial intelligence",
    "Java C++ software engineering programming",
    "Git Linux software development algorithms",
    "Python scikit-learn predictive modeling",
    "HTML CSS JavaScript responsive websites",
    "Deep learning computer vision AI models",
    "Java programming object oriented software",
]

job_categories = [
    "Data Science",
    "Data Science",
    "Web Development",
    "Web Development",
    "Machine Learning",
    "Machine Learning",
    "Software Development",
    "Software Development",
    "Data Science",
    "Web Development",
    "Machine Learning",
    "Software Development",
]

# Create ML classification model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

# Train model
model.fit(job_descriptions, job_categories)


def predict_job_category(job_description):
    prediction = model.predict([job_description])
    return prediction[0]