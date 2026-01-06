import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "phishing_model.pkl"

# Training Data (simple but effective for a demo)
emails = [
    "Your account has been suspended click the link immediately",
    "Verify your password now",
    "Your bank requires urgent verification",
    "Click here to win money",
    "You have won a lottery claim now",
    "Please find attached your invoice",
    "Meeting scheduled for tomorrow",
    "Project updates attached",
    "Team lunch at 2 PM",
]

labels = [
    1, 1, 1, 1, 1,   # phishing
    0, 0, 0, 0      # safe
]

# Simple ML pipeline
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

model = LogisticRegression()
model.fit(X, labels)

# Save model if not exists
if not os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump((model, vectorizer), f)


def load_model():
    with open(MODEL_PATH, "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer


def predict_email(text):
    """Returns ML prediction + confidence"""
    clf, vect = load_model()
    vector = vect.transform([text])
    pred = clf.predict(vector)[0]
    conf = np.max(clf.predict_proba(vector)) * 100
    return pred, round(conf, 2)


def rule_based_checks(text):
    """Detect suspicious patterns"""
    text = text.lower()
    reasons = []

    keywords = {
        "urgent": "Urgency to force quick action",
        "verify": "Asks for verification",
        "password": "Asks for password",
        "bank": "Mentions bank security",
        "click": "Pushes clicking unknown link",
        "win": "Winning money scam",
        "lottery": "Lottery scam",
        "suspended": "Account suspension scare tactics",
        "reset": "Fake password reset"
    }

    for key, msg in keywords.items():
        if key in text:
            reasons.append(msg)

    return reasons
