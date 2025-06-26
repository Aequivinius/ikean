import json
from dotenv import load_dotenv
import os
from openai import OpenAI as openai
import spacy


class Translator:

    LANGUAGES = ["en", "de", "jp"]
    TARGET_LANGUAGES = ["de", "jp"]
    LANGUAGE_NAMES = {"en": "English", "de": "German", "jp": "Japanese"}
    MODELS = { "en": "en_core_web_sm", "de": "de_core_news_sm", "jp": "ja_core_news_sm"}

    def __init__(self, translations: str):
        load_dotenv(override=True)
        self.gpt_client = openai(api_key=os.environ.get("OPENAI_API_KEY"))
        self.translations = self.load_translations(translations)
        self.models = { language: spacy.load(model_name) for language, model_name in self.MODELS.items()}

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
                "content": f"Translate into {target_language}, maintaining the markdown markup: {text}",
            },
        ]
        response = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1000,
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
                    f.write("\n" + self.translations[language]["translated"])
        return object
