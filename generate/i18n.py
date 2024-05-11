import requests
from dotenv import load_dotenv
import os

LANGUAGES = ["en", "de", "jp"]
TARGET_LANGUAGES = ["de", "jp"]
LANGUAGE_NAMES = {"en": "English", "de": "German", "jp": "Japanese"}

load_dotenv()
api_key = os.getenv("OPENAI_KEY")


def get_missing_translation(text, target_language):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": "Bearer {api_key}"},
        json={
            "prompt": f"Translate the following text to {target_language}: {text}",
            "max_tokens": 100,
            "temperature": 0.7,
            "n": 1,
            "stop": None,
        },
    )

    translated_text = response.json()["choices"][0]["text"].strip()

    return translated_text


def get_missing_translations(toy):
    for language in TARGET_LANGUAGES:
        if language not in toy["description"]:
            toy["description"][language] = get_missing_translation(
                toy["description"]["en"], language
            )
            with open(os.path.join("toys", toy.id, "{language}.md")) as f:
                f.write(toy["description"][language])
    return toy
