import os
import json
import pytest
from generate import toy_from_directory


@pytest.fixture
def sample_toys_directory(tmpdir):
    # Create a temporary directory for testing
    test_dir = tmpdir.mkdir("sample_toys")
    toy_dir1 = test_dir.mkdir("ryouhi")
    toy_dir2 = test_dir.mkdir("lego")
    # Create toy.json files with test data
    toy_data1 = {"name": "Ryouhi", "description": "A toy for testing", "price": 9.99}
    toy_json1 = toy_dir1.join("toy.json")
    toy_json1.write(json.dumps(toy_data1))
    toy_data2 = {
        "name": "Lego",
        "description": "Another toy for testing",
        "price": 19.99,
    }
    toy_json2 = toy_dir2.join("toy.json")
    toy_json2.write(json.dumps(toy_data2))
    return str(test_dir)


def test_toy_from_directory(tmpdir):
    # Create a temporary directory for testing
    test_dir = tmpdir.mkdir("test_toys")
    toy_dir = test_dir.mkdir("ryouhi")

    # Create a toy.json file with test data
    toy_data = {"name": "Ryouhi", "description": "A toy for testing", "price": 9.99}
    toy_json = toy_dir.join("toy.json")
    toy_json.write(json.dumps(toy_data))

    # Create some image files in the toy directory
    toy_dir.join("jfhiosjfiorsfr-620x617.png").write("")

    # Call the toy_from_directory function
    toy = toy_from_directory(str(toy_dir))

    # Assert the expected values
    assert toy["id"] == "ryouhi"
    assert toy["name"] == "Ryouhi"
    assert toy["description"] == "A toy for testing"
    assert toy["price"] == 9.99
    assert toy["images"] == ["jfhiosjfiorsfr-620x617.png"]


import os
import json
import pytest
from generate import load_toys


def test_load_toys(tmpdir):
    # Create a temporary directory for testing
    test_dir = tmpdir.mkdir("test_toys")
    toy_dir1 = test_dir.mkdir("ryouhi")
    toy_dir2 = test_dir.mkdir("lego")

    # Create toy.json files with test data
    toy_data1 = {"name": "Ryouhi", "description": "A toy for testing", "price": 9.99}
    toy_json1 = toy_dir1.join("toy.json")
    toy_json1.write(json.dumps(toy_data1))

    toy_data2 = {
        "name": "Lego",
        "description": "Another toy for testing",
        "price": 19.99,
    }
    toy_json2 = toy_dir2.join("toy.json")
    toy_json2.write(json.dumps(toy_data2))

    # Call the load_toys function
    toys = load_toys(str(test_dir))

    # Assert the expected values
    assert len(toys) == 2

    assert toys[0]["id"] == "ryouhi"
    assert toys[0]["name"] == "Ryouhi"
    assert toys[0]["description"] == "A toy for testing"
    assert toys[0]["price"] == 9.99
    assert toys[0]["images"] == []

    assert toys[1]["id"] == "lego"
    assert toys[1]["name"] == "Lego"
    assert toys[1]["description"] == "Another toy for testing"
    assert toys[1]["price"] == 19.99
    assert toys[1]["images"] == []
