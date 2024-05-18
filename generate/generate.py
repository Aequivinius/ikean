"""
This module contains or imports render functions, which know how to use the corresponding template, and takes care of generating the pages in the different languages.
"""

from jinja2 import Environment, FileSystemLoader
import os
import generate.checkerboard as checkerboard
import generate.i18n as i18n

SITE_CONTENT = "site_content"
RENDERED_SITES = "site"
TEMPLATES = "templates"


def generate(template: str, target: str, data: dict):
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATES))
    )
    template = env.get_template(template)
    # this adds the translations
    for language in i18n.LANGUAGES:
        rendered_page = template.render(data[language])
        os.makedirs(os.path.join(RENDERED_SITES, language), exist_ok=True)

        with open(
            os.path.join(RENDERED_SITES, language, f"{target}.html"),
            "w",
            encoding="utf-8",
        ) as output_file:
            output_file.write(rendered_page)


def home(target: str, translations: dict):
    generate(
        template="home.html",
        target="home",
        data={translations},
    )


def checkerboard(target: str, translations: dict):
    fields = checkerboard.fields_from_directory(
        os.path.join(SITE_CONTENT, "checkerboard")
    )
    generate(values, language=language, page=target, fields=fields)


def playground(target: str, translations: dict):
    fields = checkerboard.fields_from_directory("toys")
    generate(
        template="toys.html",
        target="toys",
        data={translations},
    )
