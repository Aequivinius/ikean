import os
import generate.generate as generate
import generate.i18n as i18n

PAGES = {"home": generate.home, "aspects": generate.checkerboard}

translations = i18n.load_translations(os.path.join("site_content", "translations.json"))

for page, renderer in PAGES.items():
    renderer(page, translations)
