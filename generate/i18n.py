import json
from dotenv import load_dotenv
import os
from openai import OpenAI as openai


class Translator:

    LANGUAGES = ["en", "de", "jp"]
    TARGET_LANGUAGES = ["de", "jp"]
    LANGUAGE_NAMES = {"en": "English", "de": "German", "jp": "Japanese"}

    def __init__(self, translations: str):
        load_dotenv()
        self.gpt_client = openai(api_key=os.environ.get("OPENAI_KEY"))
        self.translations = self.load_translations(translations)

    def load_translations(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            translations = json.load(f)
            translations = self.invert_translations(translations)
        return translations

    def invert_translations(self, translations):
        inverted_translations = {}
        for key, value in translations.items():
            for lang, text in value.items():
                if lang not in inverted_translations:
                    inverted_translations[lang] = {}
                inverted_translations[lang][key] = text
        return inverted_translations

    def get_missing_translation(self, text, target_language):
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
        response = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.7,
            messages=messages,
        )
        return response.choices[0].message.content

    def get_missing_translations(self, object, path):
        for language in self.TARGET_LANGUAGES:
            if language not in object["content"].keys():
                object["content"][language] = self.get_missing_translation(
                    object["content"]["en"], language
                )
                with open(os.path.join(path, f"{language}.md"), "w") as f:
                    f.write(object["content"][language])
        return object
