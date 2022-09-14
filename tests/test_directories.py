import pytest
from directories import Directory, DirectoryNotExist


@pytest.fixture
def root():
    root_dir = Directory()
    root_dir.subdirectories = {
        "fruits": Directory(name="fruits", parent=root_dir),
        "vegetables": Directory(name="vegetables", parent=root_dir),
        "grains": Directory(name="grains", parent=root_dir),
    }
    return root_dir


def test_get_directory(root: Directory):
    apples = Directory(
        name="apples",
        parent=root.subdirectories["fruits"]
    )
    root.subdirectories["fruits"].subdirectories["apples"] = apples
    assert root.get_directory(root.parse_path("fruits/apples")) == apples


def test_get_directory_not_exist(root: Directory):
    with pytest.raises(DirectoryNotExist):
        root.get_directory(root.parse_path("fruits/apples"))


def test_create_directory(root: Directory):
    root.create(root.parse_path("fruits/apples"))

    assert "apples" in root.subdirectories["fruits"].subdirectories
    apples = root.subdirectories["fruits"].subdirectories["apples"]

    assert apples.name == "apples"


def test_move_directory(root: Directory):
    root.move(root.parse_path("vegetables"), root.parse_path("fruits"))

    assert "vegetables" in root.subdirectories["fruits"].subdirectories
    vegetables = root.subdirectories["fruits"].subdirectories["vegetables"]

    assert vegetables.name == "vegetables"


def test_delete_directory(root: Directory):
    root.delete(root.parse_path("vegetables"))

    assert "vegetables" not in root.subdirectories


def test_list_all(root: Directory):
    res = root.list_all()

    assert res == ['fruits', 'grains', 'vegetables']
