# Next steps
- [x] menu better
- [x] menu across languages
- [x] menu for desktop
- [x] language links
- [x] something is odd with the menu / responsive
- [ ] generate home page in all 3 languages
- [ ] better language switcher for japanese
- [ ] read markdown to add links
- [ ] uuuuunit tests!
- [ ] small footer

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
* Use `poetry shell` then `code .` to get the `poetry` environment
