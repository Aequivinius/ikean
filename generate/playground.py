import json
import os
import generate.i18n as i18n


def toy_from_directory(directory):

    with open(os.path.join(directory, "toy.json")) as f:
        toy = json.load(f)

    toy["id"] = os.path.split(directory)[-1]

    for filename in os.listdir(directory):

        # images
        if (
            filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            and "poster" not in filename.lower()
        ):
            if "images" not in toy:
                toy["images"] = []
            toy["images"].append(filename)

        # 3d model
        if "poster" in filename.lower():
            toy["poster"] = filename

        if filename.lower().endswith((".glb")):
            toy["model"] = filename

        # descriptions
        for language in i18n.LANGUAGES:
            if filename.lower() == f"{language}.md":
                with open(os.path.join(directory, filename)) as f:
                    if "description" not in toy:
                        toy["description"] = {}
                    toy["description"][language] = f.read()

    if "model" in toy and "poster" not in toy:
        raise ValueError("If a toy has a model, it must have a poster.")

    # descriptions
    # toy = i18n.get_missing_translations(toy)

    return toy


def load_toys(file_path):
    directories = [
        d
        for d in os.listdir(file_path)
        if os.path.isdir(os.path.join(file_path, d)) and d != "template"
    ]

    toys = [
        toy_from_directory(os.path.join(file_path, directory))
        for directory in directories
    ]

    return toys
