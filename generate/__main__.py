import generate.generate as generate

translations = generate.load_translations("site/templates/translations.json")
generate.generate_page("home.html", translations)
generate.generate_page("toys.html", translations)
