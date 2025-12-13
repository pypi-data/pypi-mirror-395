"""Tests for naming helpers that classify and transform file names."""
from plumb.king.naming import (
    is_image_file,
    is_thumb_name,
    is_leveled_name,
    make_leveled_name,
    logical_base_from_name,
    make_thumb_name_for_base,
)


def test_is_image_file():
    """Recognizes supported image extensions and rejects non-image ones."""
    assert is_image_file("a.jpg")
    assert is_image_file("a.JPEG")
    assert is_image_file("b.png")
    assert not is_image_file("c.txt")


def test_is_thumb_and_leveled_and_base():
    """Checks leveled/thumbnail suffix handling and logical base extraction."""
    name = "photo.jpg"
    leveled = make_leveled_name(name)
    assert leveled.endswith("_leveled.jpg")
    assert is_leveled_name(leveled)
    assert not is_leveled_name(name)

    thumb = make_thumb_name_for_base("photo", ".jpg")
    assert thumb == "photo_leveled_thumb.jpg"
    assert is_thumb_name(thumb)

    assert logical_base_from_name(thumb) == "photo"
    assert logical_base_from_name(leveled) == "photo"

    legacy_thumb = "photo_thumb.jpg"
    assert logical_base_from_name(legacy_thumb) == "photo"
