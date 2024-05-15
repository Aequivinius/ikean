# Toys
It's automatically generated for every subdirectory in `toys`. The structure is as follows:

```
toys
|-- id (for example: hanachirusato)
    |-- toy.json (fixed name)
    |-- en.md (fixed name)
    |-- de.md
    |-- jp.md
    |-- photo1.jpg (name is not important)
    |-- ... (more photos)
    |-- model.glb (needs to end in .glb)
    |-- poster.jpg (needs to be called poster)
|-- id (for example: ryouhi)
    |-- ...
```

The `toy.json` at least contains (also see `toys/template/toy.json`):

```json
{
    "category": "chashaku",
    "name": {
        "en": "Ryouhi",
        "de": "Ryouhi",
        "jp": "両樋"
    },
    "price": 80,
    "on_sale": true,
    "maker": {
        "en": "Rikyu",
        "de": "Rikyu",
        "jp": "利休"
    }
}
```

The `.md` files also support `[[wikilinks]]`, which will point to [tea.hedonisms.ch](https://tea.hedonisms.ch/wiki).

# Translations
* the `generate.py` creates multilingual sites based on the `templates/translations.json`. The latter has the following format:

```json
{ "key" : { "de" : "Lohrem ipsett dohler amen.",
            "en" : "Lorem ipsum dolor amet.",
            "jp" : "ロレム　イップスム　ドロル　アメト。"} }
```

It is converted by `generate.py` into a different format where `key`s are sorted *under* `language`.

# CSS
* stick to [BEM](https://getbem.com/introduction/) naming convention
* we're following a mobile-first approach, so all desktop styling lives in `styles-768.css`

# Dev
* Use `poetry shell` then `code .` to get the `poetry` environment in VS Code
