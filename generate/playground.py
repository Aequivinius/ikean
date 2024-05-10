import json
import os


def toy_from_directory(directory):

    with open(os.path.join(directory, "toy.json")) as f:
        toy = json.load(f)

    toy["id"] = os.path.split(directory)[-1]

    for filename in os.listdir(directory):
        if (
            filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            and "poster" not in filename.lower()
        ):
            if "images" not in toy:
                toy["images"] = []
            toy["images"].append(filename)

        if "poster" in filename.lower():
            toy["poster"] = filename

        if filename.lower().endswith((".glb")):
            toy["model"] = filename

    if "model" in toy and "poster" not in toy:
        raise ValueError("If a toy has a model, it must have a poster.")

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
