"""Tests for EXIF utilities and color mode normalization.

Ensures images load with EXIF orientation applied and mode normalization keeps
L images and converts others to RGB.
"""
from PIL import Image
from plumb.king.exif_utils import load_image_exif_corrected, normalize_mode


def test_load_image_exif_corrected_opens_file(sample_image_path):
    """load_image_exif_corrected returns a PIL Image with expected size."""
    img = load_image_exif_corrected(sample_image_path)
    assert isinstance(img, Image.Image)
    # Should keep expected size
    assert img.size == (640, 360)


def test_normalize_mode_converts_non_rgb():
    rgba = Image.new("RGBA", (10, 10), (10, 20, 30, 128))
    out = normalize_mode(rgba)
    assert out.mode == "RGB"

    gray = Image.new("L", (10, 10), 128)
    out2 = normalize_mode(gray)
    assert out2.mode == "L"
