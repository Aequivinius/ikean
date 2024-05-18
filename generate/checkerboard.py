import os
import json
import generate.i18n as i18n
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension


def fields_from_directory(directory):
    subdirectories = [
        d
        for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d)) and d != "template"
    ]
    fields = [
        field_from_directory(os.path.join(directory, subdirectory))
        for subdirectory in subdirectories
    ]
    return fields


def field_from_directory(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
    if len(json_files) != 1:
        raise ValueError("There should be exactly one JSON file in the directory.")

    with open(os.path.join(directory, json_files[0])) as f:
        field = json.load(f)

    field["id"] = os.path.split(directory)[-1]

    for filename in os.listdir(directory):

        # images
        if (
            filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            and "poster" not in filename.lower()
        ):
            if "images" not in field:
                field["images"] = []
            field["images"].append(filename)

        # content
        if filename.lower().endswith(".md"):
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

    if "model" in field and "poster" not in field:
        raise ValueError("If a toy has a model, it must have a poster.")

    field["images"] = sorted(field["images"])

    # field = i18n.get_missing_translations(field, "toys")

    return field
