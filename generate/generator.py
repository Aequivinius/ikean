from jinja2 import Environment, FileSystemLoader
import os
from generate.i18n import Translator
import json
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from datetime import datetime

"""This package generates the site in different languages, loading its contents either from translations.json and directories.

For every templates/*.html file, it will generate a page in each i18n.LANGUAGES language. Normally, it will use the contents from translation.json, but if the page is in the CHECKERBOARDS list in the corresponding .json, it will load the contents from the corresponding directory."""

PAGES = "site"
TEMPLATES = "templates"
PAGE_TYPES = "pages.json"
CONTENT = "content"


class Generator:
    def __init__(self):
        self.TEMPLATES = os.path.join(os.path.dirname(__file__), TEMPLATES)
        with open(os.path.join(self.TEMPLATES, PAGE_TYPES)) as f:
            self.page_types = json.load(f)
        self.env = Environment(loader=FileSystemLoader(self.TEMPLATES))
        self.env.filters["format_date"] = self.format_date
        self.translator = Translator(os.path.join(CONTENT, "translations.json"))

    def format_date(self, date_str, language="jp"):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if language == "jp":
            format = date_obj.strftime("%d日%m月%Y年")
        if language == "en":
            format = date_obj.strftime("%B %d, %Y")
        if language == "de":
            format = date_obj.strftime("%d.%m.%Y")
        return format

    def generate(self, template_file: str, isCheckerboard: bool):
        template = self.env.get_template(f"{template_file}.html")
        for language in Translator.LANGUAGES:
            fields = None
            if isCheckerboard:
                fields = self.fields_from_directory(
                    os.path.join(CONTENT, template_file)
                )
            page = template.render(
                {
                    **self.translator.translations[language],
                    "language": language,
                    "page": template_file,
                    "fields": fields,
                    "categories": self.categories_from_fields(fields),
                }
            )
            with open(
                os.path.join(PAGES, language, f"{template_file}.html"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(page)

    def categories_from_fields(self, fields):
        if fields is None:
            return []
        categories = []
        for field in fields:
            if "category" in field:
                if field["category"] not in categories:
                    categories.append(field["category"])
        return categories

    def fields_from_directory(self, directory):
        subdirectories = [
            d
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d)) and d != "template"
        ]

        if len(subdirectories) == 0:
            return [self.field_from_directory(directory)]

        fields = [
            self.field_from_directory(os.path.join(directory, subdirectory))
            for subdirectory in subdirectories
        ]
        return fields

    def field_from_directory(self, directory):
        print(directory)
        json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
        if len(json_files) != 1:
            raise ValueError("There should be exactly one JSON file in the directory.")
        with open(os.path.join(directory, json_files[0])) as f:
            field = json.load(f)
        field["id"] = os.path.split(directory)[-1]

        field["images"] = sorted(
            [
                f
                for f in os.listdir(directory)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
                and "poster" not in f.lower()
            ]
        )

        posters = [f for f in os.listdir(directory) if "poster" in f.lower()]
        if posters:
            field["poster"] = posters[0]

        model = [f for f in os.listdir(directory) if f.lower().endswith((".glb"))]
        if len(model) > 0:
            field["model"] = model[0]

        if "model" in field and "poster" not in field:
            raise ValueError("If a toy has a model, it must have a poster.")

        if "category" in field:
            id = field["category"]
            field["category"] = {
                l: self.translator.translations[l][id] for l in Translator.LANGUAGES
            }
            field["category"]["id"] = id

        for filename in [f for f in os.listdir(directory) if f.lower().endswith(".md")]:
            language = filename.split(".")[0]
            with open(os.path.join(directory, filename)) as f:
                markdown_content = f.read()
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=[
                        "tables",
                        "abbr",
                        WikiLinkExtension(base_url="https://tea.hedonisms.ch/wiki/"),
                    ],
                )
                if "content" not in field:
                    field["content"] = {}
                field["content"][language] = html_content

        field = self.translator.get_missing_translations(field, directory)
        return field
