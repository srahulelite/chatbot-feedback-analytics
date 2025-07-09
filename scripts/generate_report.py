import json
from collections import Counter, defaultdict

INPUT_PATH = "data/cleaned/chatbot_feedback_cleaned.json"

def load_cleaned_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report(data):
    rating_sum = 0
    lang_counter = Counter()
    tag_counter = Counter()
    gender_sessions = defaultdict(list)

    for record in data:
        rating_sum += record["feedback"]["rating"]
        lang_counter[record["feedback"]["language"]] += 1
        tag_counter.update(record["feedback"]["tags"])
        gender_sessions[record["user"]["gender"]].append(record["session_id"])

    avg_rating = rating_sum / len(data) if data else 0

    print("\n========== FEEDBACK INSIGHT REPORT ==========")
    print(f"Total Valid Records: {len(data)}")
    print(f"Average Rating: {avg_rating:.2f}\n")

    print("Feedback Count Per Language:")
    for lang, count in lang_counter.items():
        print(f"  {lang.upper()} → {count}")

    print("\nMost Common Feedback Tags:")
    for tag, count in tag_counter.most_common(5):
        print(f"  {tag} → {count} times")

    print("\nSessions Grouped By Gender:")
    for gender, sessions in gender_sessions.items():
        print(f"  {gender.upper()} ({len(sessions)} sessions): {sessions[:5]}{' ...' if len(sessions) > 5 else ''}")  # Limit preview

def main():
    data = load_cleaned_data(INPUT_PATH)
    generate_report(data)

if __name__ == "__main__":
    main()
