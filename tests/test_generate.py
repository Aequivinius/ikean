import pytest
from generate.generate import load_translations, invert_translations, generate_page
import json


@pytest.fixture
def translations_file(tmp_path):
    translations_dir = tmp_path / "translations"
    translations_dir.mkdir()

    translations_file = translations_dir / "translations.json"
    translations_file.write_text(
        '{"hello": {"en": "Hello", "de": "Hallo", "jp": "こんにちは"}, "goodbye": {"en": "Goodbye", "de": "Auf Wiedersehen", "jp": "さようなら"}, "thank_you": {"en": "Thank you", "de": "Danke", "jp": "ありがとうございます"}'
    )

    yield translations_file

    translations_dir.rmdir()


def test_load_translations(translations_file):
    # Test case 1: Valid file path
    translations = load_translations(translations_file)
    assert isinstance(translations, dict)
    assert len(translations) > 0
    # Test case 2: Non-existent file path
    with pytest.raises(FileNotFoundError):
        load_translations("nonexistent.json")
    # Test case 3: Invalid file format
    with pytest.raises(json.JSONDecodeError):
        load_translations("invalid.json")


def test_load_translations():
    # Test case 1: Valid file path
    translations = load_translations("translations.json")
    assert isinstance(translations, dict)
    assert len(translations) > 0

    # Test case 2: Non-existent file path
    with pytest.raises(FileNotFoundError):
        load_translations("nonexistent.json")

    # Test case 3: Invalid file format
    with pytest.raises(json.JSONDecodeError):
        load_translations("invalid.json")


def test_invert_translations():
    # Test case 1: Empty translations
    translations = {}
    inverted_translations = invert_translations(translations)
    assert inverted_translations == {}

    # Test case 2: Single translation
    translations = {"hello": {"en": "Hello"}}
    inverted_translations = invert_translations(translations)
    assert inverted_translations == {"en": {"hello": "Hello"}}

    # Test case 3: Multiple translations
    translations = {
        "hello": {"en": "Hello", "de": "Hallo", "fr": "Bonjour"},
        "goodbye": {"en": "Goodbye", "de": "Auf Wiedersehen", "fr": "Au revoir"},
        "thank_you": {"en": "Thank you", "de": "Danke", "fr": "Merci"},
    }
    inverted_translations = invert_translations(translations)
    assert inverted_translations == {
        "en": {"hello": "Hello", "goodbye": "Goodbye", "thank_you": "Thank you"},
        "de": {"hello": "Hallo", "goodbye": "Auf Wiedersehen", "thank_you": "Danke"},
        "fr": {"hello": "Bonjour", "goodbye": "Au revoir", "thank_you": "Merci"},
    }

    # Test case 4: Duplicate translations
    translations = {
        "hello": {"en": "Hello", "de": "Hallo", "fr": "Bonjour"},
        "goodbye": {"en": "Goodbye", "de": "Auf Wiedersehen", "fr": "Au revoir"},
        "thank_you": {"en": "Thank you", "de": "Danke", "fr": "Merci"},
        "hi": {"en": "Hello", "de": "Hallo", "fr": "Bonjour"},
    }
    inverted_translations = invert_translations(translations)
    assert inverted_translations == {
        "en": {
            "hello": "Hello",
            "goodbye": "Goodbye",
            "thank_you": "Thank you",
            "hi": "Hello",
        },
        "de": {
            "hello": "Hallo",
            "goodbye": "Auf Wiedersehen",
            "thank_you": "Danke",
            "hi": "Hallo",
        },
        "fr": {
            "hello": "Bonjour",
            "goodbye": "Au revoir",
            "thank_you": "Merci",
            "hi": "Bonjour",
        },
    }


def test_generate_page(tmp_path):
    # Create a temporary directory for testing
    test_dir = tmp_path / "test"
    test_dir.mkdir()

    # Create a temporary template file
    template_file = test_dir / "template.html"
    template_file.write_text("<html><body>{{ value }}</body></html>")

    # Create a temporary translations dictionary
    translations = {
        "en": {"value": "Hello"},
        "fr": {"value": "Bonjour"},
        "de": {"value": "Hallo"},
    }

    # Call the generate_page function
    generate_page(str(template_file), translations)

    # Check if the output files are generated correctly
    for language in translations.keys():
        output_file = test_dir / language / "template.html"
        assert output_file.exists()

        with open(output_file, "r") as f:
            content = f.read()
            assert translations[language]["value"] in content

    # Clean up the temporary directory
    test_dir.rmdir()


if __name__ == "__main__":
    pytest.main()
