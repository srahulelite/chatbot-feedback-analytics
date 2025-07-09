import json
import os
from collections import Counter

INPUT_PATH = "data/synthetic/chatbot_feedback_1000.json"
OUTPUT_PATH = "data/cleaned/chatbot_feedback_cleaned.json"

def is_valid_int(val, min_val=None, max_val=None):
    try:
        num = int(val)
        if (min_val is not None and num < min_val) or (max_val is not None and num > max_val):
            return False
        return True
    except:
        return False

def clean_feedback(raw_data):
    cleaned_data = []
    for record in raw_data:
        try:
            rating = int(record["feedback"]["rating"]) if is_valid_int(record["feedback"]["rating"], 1, 5) else None
            gender = record["user"]["gender"].strip().lower()
            language = record["feedback"]["language"].strip().lower()
            tags = record["feedback"].get("tags", [])

            if gender not in ["m", "f"]:
                raise ValueError("Invalid gender")

            if language not in ["en", "fr", "es"]:
                raise ValueError("Invalid language")

            if rating is None:
                raise ValueError("Invalid rating")

            clean_record = {
                "session_id": record["session_id"],
                "user": {
                    "id": record["user"]["id"],
                    "gender": gender
                },
                "feedback": {
                    "rating": rating,
                    "comment": record["feedback"]["comment"].strip() or "No comment",
                    "language": language,
                    "tags": [tag.lower() for tag in tags] if isinstance(tags, list) else []
                }
            }

            cleaned_data.append(clean_record)

        except Exception as e:
            continue  # Skip bad records silently (can log if needed)

    return cleaned_data

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Input file not found: {INPUT_PATH}")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = clean_feedback(raw_data)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Cleaned {len(cleaned)} records saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
