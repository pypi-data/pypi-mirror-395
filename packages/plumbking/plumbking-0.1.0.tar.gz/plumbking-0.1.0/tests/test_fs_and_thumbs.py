"""Tests for filesystem scanning and thumbnail planning/creation.

Validates classification of files into candidates/leveled/thumbs/others and
ensures thumbnails are planned and generated with correct sizing constraints.
"""
from PIL import Image

from plumb.king.fs_scanner import discover_images
from plumb.king.naming import make_leveled_name, make_thumb_name_for_base
from plumb.king.thumbnails import plan_thumbnails, create_thumbnail


def test_discover_images_and_thumbs(tmp_images_dir):
    """discover_images classifies files correctly; planning skips existing thumbs."""
    # Create files
    img1 = tmp_images_dir / "a.jpg"
    Image.new("RGB", (64, 48), (200, 200, 200)).save(img1)

    leveled_name = make_leveled_name("a.jpg")
    img1_lev = tmp_images_dir / leveled_name
    Image.new("RGB", (64, 48), (220, 220, 220)).save(img1_lev)

    thumb_name = make_thumb_name_for_base("a", ".jpg")
    thumb_file = tmp_images_dir / thumb_name
    Image.new("RGB", (32, 24), (128, 128, 128)).save(thumb_file)

    (tmp_images_dir / "not_image.txt").write_text("hello")
    (tmp_images_dir / "sub").mkdir()

    candidates, leveled, thumbs, others = discover_images(str(tmp_images_dir))

    assert "a.jpg" in candidates
    assert leveled_name in leveled
    assert thumb_name in thumbs
    assert "not_image.txt" in others
    assert "sub" in others

    # Plan thumbnails should skip because already exists for base/extension
    ops = plan_thumbnails(str(tmp_images_dir), ["a.jpg", leveled_name], [thumb_name])
    assert ops == []


def test_create_thumbnail(tmp_images_dir):
    """create_thumbnail writes a file whose longest side does not exceed max_size."""
    src = tmp_images_dir / "b.png"
    Image.new("RGB", (1600, 400), (0, 120, 255)).save(src)

    dst = tmp_images_dir / "b_leveled_thumb.png"
    max_size = 200
    create_thumbnail(str(src), str(dst), max_size)

    assert dst.exists()
    img = Image.open(dst)
    w, h = img.size
    assert max(w, h) <= max_size
