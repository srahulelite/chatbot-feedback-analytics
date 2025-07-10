from faker import Faker
import random
import json
from datetime import datetime
import uuid

# Setup
fake = Faker()
Faker.seed(42)
random.seed(42)

# Supported languages and some sample feedback templates per language
languages = {
    "en": {
        "comments": ["Great service!", "Very helpful.", "Too slow", "Confusing at times", "Loved it!", "No comment"],
        "tags": ["Helpful", "Quick", "Polite", "Slow", "Confusing", "Accurate"]
    },
    "fr": {
        "comments": ["Service excellent", "Très utile", "Trop lent", "Déroutant parfois", "J'ai adoré", "Aucun commentaire"],
        "tags": ["Utile", "Rapide", "Poli", "Lent", "Confus", "Précis"]
    },
    "es": {
        "comments": ["Servicio excelente", "Muy útil", "Demasiado lento", "Confuso a veces", "Me encantó", "Sin comentarios"],
        "tags": ["Útil", "Rápido", "Educado", "Lento", "Confuso", "Preciso"]
    }
}

genders = ["m", "f", "x"]  # x will be filtered out later

def generate_feedback_record(session_num):
    lang = random.choice(list(languages.keys()))
    gender = random.choice(genders)

    record = {
        "session_id": f"S{1000 + session_num}",
        "user": {
            "id": f"U{1000 + session_num}",
            "gender": gender
        },
        "feedback": {
            "rating": str(random.choice([1, 2, 3, 4, 5, "NaN"])),  # Some invalid ratings
            "comment": random.choice(languages[lang]["comments"]),
            "language": lang.upper() if random.random() < 0.5 else lang,  # Some upper, some lower
            "tags": random.sample(languages[lang]["tags"], k=random.randint(1, 3))
        }
    }
    return record

# Generate 1000 synthetic records
synthetic_data = [generate_feedback_record(i) for i in range(1000)]

# Save to file
output_path = "data/synthetic/chatbot_feedback_1000.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(synthetic_data, f, indent=2, ensure_ascii=False)

output_path
