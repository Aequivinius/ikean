import json
from dotenv import load_dotenv
import os
from openai import OpenAI as openai


LANGUAGES = ["en", "de", "jp"]
TARGET_LANGUAGES = ["de", "jp"]
LANGUAGE_NAMES = {"en": "English", "de": "German", "jp": "Japanese"}

load_dotenv()
gpt_client = openai(api_key=os.environ.get("OPENAI_KEY"))


def load_translations(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        translations = json.load(f)
        translations = invert_translations(translations)
    return translations


def invert_translations(translations):
    inverted_translations = {}
    for key, value in translations.items():
        for lang, text in value.items():
            if lang not in inverted_translations:
                inverted_translations[lang] = {}
            inverted_translations[lang][key] = text
    return inverted_translations


def get_missing_translation(text, target_language):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for text translation.",
        },
        {
            "role": "user",
            "content": f"Translate into {target_language}, stripping any <p>-tags: {text}",
        },
    ]

    response = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        temperature=0.7,
        messages=messages,
    )

    return response.choices[0].message.content


def get_missing_translations(toy):
    for language in TARGET_LANGUAGES:
        if language not in toy["description"]:
            toy["description"][language] = get_missing_translation(
                toy["description"]["en"], language
            )
            with open(os.path.join("toys", toy["id"], f"{language}.md"), "w") as f:
                f.write(toy["description"][language])
    return toy
