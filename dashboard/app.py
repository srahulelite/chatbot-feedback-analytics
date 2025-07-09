import os
import json
from flask import Flask, render_template
from collections import Counter

app = Flask(__name__)

# Absolute path to cleaned + sentiment dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned", "chatbot_feedback_with_sentiment.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    records = json.load(f)

# KPI Calculations
total_feedback = len(records)
avg_rating = round(sum([r["feedback"]["rating"] for r in records]) / total_feedback, 2)
positive_count = sum(1 for r in records if r["feedback"]["sentiment"] == "positive")
negative_count = sum(1 for r in records if r["feedback"]["sentiment"] == "negative")

positive_percent = round((positive_count / total_feedback) * 100, 2)
negative_percent = round((negative_count / total_feedback) * 100, 2)

sentiment_data = Counter(
    r["feedback"]["sentiment"]["label"]
    for r in records
    if "sentiment" in r["feedback"] and "label" in r["feedback"]["sentiment"]
)
language_data = Counter(r["feedback"]["language"] for r in records)

@app.route("/")
def index():
    return render_template("index.html",
                           records=records,
                           total_feedback=total_feedback,
                           avg_rating=avg_rating,
                           positive_percent=positive_percent,
                           negative_percent=negative_percent,
                           sentiment_data=sentiment_data,
                           language_data=language_data)



@app.route("/dashboard")
def dashboard():
    with open("data/cleaned/chatbot_feedback_with_sentiment.json") as f:
        records = json.load(f)

    gender_counts = Counter(r["user"]["gender"] for r in records)
    lang_counts = Counter(r["feedback"]["language"] for r in records)
    sentiment_counts = Counter(r["feedback"]["sentiment"]["label"] for r in records)

    return render_template("dashboard.html",
                           gender=gender_counts,
                           language=lang_counts,
                           sentiment=sentiment_counts)


if __name__ == "__main__":
    app.run(debug=True)
