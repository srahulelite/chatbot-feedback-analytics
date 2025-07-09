import json
from textblob import TextBlob

INPUT_PATH = "data/cleaned/chatbot_feedback_cleaned.json"
OUTPUT_PATH = "data/cleaned/chatbot_feedback_with_sentiment.json"

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # [-1.0 to 1.0]
    if polarity > 0.2:
        label = "Positive"
    elif polarity < -0.2:
        label = "Negative"
    else:
        label = "Neutral"
    return {"score": round(polarity, 3), "label": label}

def process_feedback_with_sentiment(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    for record in data:
        comment = record["feedback"]["comment"]
        sentiment = analyze_sentiment(comment)
        record["feedback"]["sentiment"] = sentiment

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)

    print(f"Sentiment-augmented data written to {output_path}")

if __name__ == "__main__":
    process_feedback_with_sentiment(INPUT_PATH, OUTPUT_PATH)
