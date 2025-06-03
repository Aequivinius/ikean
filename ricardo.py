import os
import json
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup


# --- CONFIGURATION ---
root_directory = 'content/utensils'  # Update this
translations_path = 'content/translations.json'  # Update this
output_excel = 'output.xlsx'
jpg_folder_name = 'jpg'
tea_paragraph = "Dieses Utensil ist für die japanische Teezeremonie bestimmt."

# --- LOAD TRANSLATIONS ---
with open(translations_path, 'r', encoding='utf-8') as f:
    translations = json.load(f)

def translate_category(category_key):
    return translations.get(category_key, {}).get('de', category_key)

def html_to_plain_text(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # Handle <abbr title="">text</abbr>
    for abbr in soup.find_all('abbr'):
        title = abbr.get('title')
        if title:
            abbr.replace_with(f"{abbr.get_text()} ({title})")
        else:
            abbr.replace_with(abbr.get_text())

    return soup.get_text(separator=' ', strip=True)

# --- COLLECT DATA ---
entries = []

for subdir in os.listdir(root_directory):
    subdir_path = os.path.join(root_directory, subdir)
    if not os.path.isdir(subdir_path):
        continue

    toy_path = os.path.join(subdir_path, 'toy.json')
    de_md_path = os.path.join(subdir_path, 'de.md')

    if not (os.path.exists(toy_path) and os.path.exists(de_md_path)):
        continue

    with open(toy_path, 'r', encoding='utf-8') as f:
        toy = json.load(f)

    if not toy.get('sale', False):
        continue  # 🔁 Skip this item if it's not for sale

    with open(de_md_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()
        plain_text = html_to_plain_text(raw_md)
        beschreibung = f"{plain_text}\n\n{tea_paragraph}"

    category_de = translate_category(toy.get('category', ''))
    name_de = toy.get('name', {}).get('de', '')
    name_jp = toy.get('name', {}).get('jp', '')
    maker = toy.get('maker', {}).get('de', '')

    titel = f"{category_de} {name_de} ({name_jp})"
    if maker:
        titel += f", gemacht von {maker}"

    # Convert .webp to .jpg
    images_converted = False
    jpg_dir = os.path.join(subdir_path, jpg_folder_name)
    os.makedirs(jpg_dir, exist_ok=True)

    for file in os.listdir(subdir_path):
        if file.lower().endswith('.webp'):
            webp_path = os.path.join(subdir_path, file)
            jpg_path = os.path.join(jpg_dir, os.path.splitext(file)[0] + '.jpg')
            try:
                img = Image.open(webp_path).convert('RGB')
                img.save(jpg_path, 'JPEG')
                images_converted = True
            except Exception as e:
                print(f"Error converting {webp_path}: {e}")

    entries.append({
        'Titel': titel,
        'Refernz-Nr.': subdir,
        'Beschreibung': beschreibung
    })

# --- WRITE TO EXCEL ---
df = pd.DataFrame(entries)
df.to_excel(output_excel, index=False)
print(f"Excel file saved to: {output_excel}")
