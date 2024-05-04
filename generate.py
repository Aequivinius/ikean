import json
from jinja2 import Environment, FileSystemLoader
import os
import os


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


def generate_page(template_file, translations):
    env = Environment(loader=FileSystemLoader("src/templates/"))
    template = env.get_template(template_file)

    for language, value in translations.items():
        rendered_template = template.render(value, language=language, page="index.html")
        os.makedirs(os.path.join("src", language), exist_ok=True)

        with open(
            os.path.join("src", language, "index.html"), "w", encoding="utf-8"
        ) as output_file:
            output_file.write(rendered_template)


if __name__ == "__main__":
    translations = load_translations("src/templates/translations.json")
    generate_page("index.html", translations)
