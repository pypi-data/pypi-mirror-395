"""Tests for high-level leveling application functions.

This module validates:
- rotate_and_crop: rotation and maximal inscribed rectangle crop
- compute_leveling_angle_from_thumbnail: angle estimation on a thumbnail crop
- level_image_final: end-to-end leveling that preserves output size
It also provides a helper to measure dominant roll using Canny+Hough.
"""
import math
import numpy as np
from PIL import Image

from plumb.king.leveling_apply import (
    rotate_and_crop,
    compute_leveling_angle_from_thumbnail,
    level_image_final,
)
from plumb.king.leveling_core import (
    to_canny,
    to_hough_lines,
    line_angles_and_lengths,
    epsilon_find_weighted,
)
from .conftest import make_horizon_image, rotate_image


def dominant_roll_angle_deg(img: Image.Image, max_correction_deg=20):
    """Compute dominant roll angle (degrees) via Canny+Hough aggregation.

    Used in assertions to verify that leveled images are near-horizontal.
    """
    gray = img.convert("L")
    edges = to_canny(gray, blur_ksize=9, low_thresh=50, high_thresh=150, use_variance_mask=False)
    lines = to_hough_lines(edges)
    if lines.shape[0] == 0:
        return 0.0
    angles, lengths = line_angles_and_lengths(lines)
    s, c = epsilon_find_weighted(angles, lengths, p=1.5, max_angle_deg=max_correction_deg)
    phi = math.degrees(math.atan2(s, c))
    return float(phi)


def test_rotate_and_crop_preserves_content_bounds():
    """Rotating and cropping should reduce both width and height (non-zero angle)."""
    img = make_horizon_image(size=(300, 200), line_thickness=10)
    phi = math.radians(10)
    out = rotate_and_crop(img, phi)
    # Should reduce size (since cropping occurs for non-zero angle)
    assert out.size[0] < img.size[0]
    assert out.size[1] < img.size[1]


def test_compute_leveling_angle_from_thumbnail_estimates_rotation():
    """Angle estimated from thumbnail should match the injected rotation within tolerance."""
    base = make_horizon_image(size=(600, 400), line_thickness=6)
    injected_deg = 8.0
    rotated = rotate_image(base, injected_deg)

    est = compute_leveling_angle_from_thumbnail(rotated, analysis_size=480, max_correction_deg=15)
    est_deg = math.degrees(est)
    # Should approximately equal the injected rotation (same sign)
    assert abs(est_deg - injected_deg) < 6.0


ess_tol_deg = 2.5


def test_level_image_final_levels_horizon_and_preserves_size():
    """End-to-end leveling should preserve canvas size and reduce residual roll."""
    base = make_horizon_image(size=(640, 360), line_thickness=6)
    injected_deg = -7.5
    rotated = rotate_image(base, injected_deg)

    leveled = level_image_final(rotated)

    # Size must be preserved
    assert leveled.size == rotated.size

    # Dominant roll after leveling should be near 0
    roll_after = dominant_roll_angle_deg(leveled, max_correction_deg=15)
    assert abs(roll_after) < ess_tol_deg
