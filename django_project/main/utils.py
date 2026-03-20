import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


def load_bad_words():
    """Reads the bad-words.txt file from the project root."""
    file_path = os.path.join(settings.BASE_DIR, 'bad-words.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print("Warning: bad-words.txt not found in project root!")
        return set()


BAD_WORDS_SET = load_bad_words()


def is_message_appropriate(text):
    if not text or not text.strip():
        return False

    lowercase_text = text.lower()
    clean_text = "".join(char if char.isalnum()
                         or char.isspace() else " " for char in lowercase_text)
    words_in_message = clean_text.split()

    for word in words_in_message:
        if word in BAD_WORDS_SET:
            print(f"DEBUG: Blocked by List check ('{word}')")
            return False

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = (
            "You are a strict content moderator. "
            "Reply ONLY with 'REJECT' if this message is rude, toxic, "
            "insulting, or contains hidden profanity. "
            "Reply 'APPROVE' if it is a normal message. "
            f"Message: {text}"
        )

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.0}
        )

        if not response or not response.text:
            return False

        result = response.text.strip().upper()
        return "APPROVE" in result

    except Exception as e:
        print(f"AI ERROR: {e}")
        return True