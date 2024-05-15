import generate.generate as generate
import generate.i18n as i18n

translations = i18n.load_translations("site/templates/translations.json")
generate.generate_page("home.html", translations)
generate.generate_page("toys.html", translations)
generate.generate_page("order.html", translations)
