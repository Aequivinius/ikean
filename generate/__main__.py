from generate.generator import Generator
from generate.generator import CONTENT

import sys
import os
import json
import pdfkit
from datetime import datetime
import zipfile

def generate():
    generator = Generator()
    for template, type in generator.page_types.items():
        generator.generate(template, type == "checkerboard")

def sell(items):
    """ Doesn't work yet!  """
    UTENSILS_PATH = os.path.join(os.getcwd(), CONTENT, "utensils")
    current_date = datetime.now().strftime("%d%m%Y")
    sale_directory = f"sale_{current_date}"
    if not os.path.exists(sale_directory):
        os.makedirs(sale_directory)


    pdfkit_options = {
        'print-media-type': '',
        'enable-local-file-access': None
    }

    for item in items:
        item_path = os.path.join(UTENSILS_PATH, item)
        if os.path.isdir(item_path):
            item_json = json.load(open(os.path.join(item_path, "toy.json")))
            if not item_json["sale"]:
                raise ValueError(f"Item '{item}' is already sold.")
        else:
            raise FileNotFoundError(f"Directory for item '{item}' does not exist in {UTENSILS_PATH}.")

        # it's not printing using the css
        pdfkit.from_url(f'https://www.ikean.ch/site/de/utensils.html#{item}', f'{sale_directory}/{item}.pdf', options=pdfkit_options)

    zip_name = f"{sale_directory}.zip"
    try:
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(sale_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, sale_directory))
        print(f"'{sale_directory}' successfully zipped into '{zip_name}'.")
    except Exception as e:
        print(f"Error while zipping '{sale_directory}': {e}")

    # HTML('url').write_pdf('sale.pdf')
    # print the websites
    # count together their prices
    # total to ebill
    # set sale to false
    # change display

    print(f"Selling the following items: {', '.join(items)}")

def main():
    if len(sys.argv) < 2:
        generate()

    else:

        command = sys.argv[1]
        if command == "generate":
            generate()
        elif command == "sell":
            if len(sys.argv) < 3:
                print("Usage: python -m sell <name> <name> ...")
                sys.exit(1)
            items = sys.argv[2:]
            sell(items)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

if __name__ == "__main__":
    main()
