"""Unit tests for core leveling primitives.

Covers k-means segmentation, variance masking + Canny, Hough line extraction,
angle aggregation, and the multiscale roll estimator.
"""
import math
import numpy as np
from PIL import Image, ImageDraw

from plumb.king.leveling_core import (
    kmeans_segment_gray,
    variance_mask,
    to_canny,
    to_hough_lines,
    line_angles_and_lengths,
    epsilon_find_weighted,
    estimate_roll_multiscale_kmeans,
)
from .conftest import make_horizon_image, rotate_image


def make_diagonal_image(size=(320, 240), thickness=4):
    """Create a simple image with a horizontal line (used for Hough tests)."""
    w, h = size
    img = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(img)
    for t in range(-thickness//2, thickness//2 + 1):
        d.line([(0, h//2 + t), (w-1, h//2 + t)], fill=(0, 0, 0), width=1)
    return img


def test_kmeans_segment_gray_two_clusters():
    """K-means with k=2 should segment a bi-color image into two gray labels."""
    # Create simple bi-color image
    img = Image.new("RGB", (100, 50), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 49, 49], fill=(0, 0, 0))
    seg = kmeans_segment_gray(img, k=2, pre_blur_ksize=3, rng_seed=123)
    assert seg.shape == (50, 100)
    values = np.unique(seg)
    assert values.size == 2


def test_variance_mask_and_canny_detects_line():
    """Variance mask shape matches input; Canny finds edges on synthetic horizon."""
    img = make_horizon_image(size=(200, 120), line_thickness=4)
    arr = np.array(img.convert("L"))
    mask = variance_mask(arr, ksize=9, quantile=0.5)
    assert mask.shape == arr.shape

    edges = to_canny(arr, blur_ksize=7, low_thresh=40, high_thresh=120, use_variance_mask=False)
    assert edges.dtype == np.uint8
    assert edges.shape == arr.shape
    assert (edges > 0).sum() > 0


def test_hough_lines_and_angles():
    img = make_horizon_image(size=(300, 200), line_thickness=6)
    edges = to_canny(img.convert("L"), blur_ksize=9, use_variance_mask=False)
    lines = to_hough_lines(edges)
    assert lines.shape[1] == 4
    assert lines.shape[0] >= 1

    angles, lengths = line_angles_and_lengths(lines)
    assert angles.shape == (lines.shape[0],)
    assert lengths.min() > 0

    s, c = epsilon_find_weighted(angles, lengths, p=1.2, max_angle_deg=15)
    phi_deg = math.degrees(math.atan2(s, c))
    # For a horizontal line, roll should be ~0
    assert abs(phi_deg) < 2.0


def test_estimate_roll_multiscale_kmeans_matches_rotation():
    base = make_horizon_image(size=(480, 320), line_thickness=5)
    injected = 9.0
    rot = rotate_image(base, injected)

    # crop is internal to compute function; here directly using multiscale on crop_img
    # mimic the crop used in compute_leveling_angle_from_thumbnail by cropping borders a bit
    thumb = rot.copy()
    thumb.thumbnail((400, 400), Image.BICUBIC)
    w, h = thumb.size
    crop = thumb.crop((int(w*0.15), int(h*0.2), int(w*0.85), int(h*0.8)))

    est = estimate_roll_multiscale_kmeans(crop, max_correction_deg=15)
    est_deg = math.degrees(est)
    assert abs(est_deg - injected) < 4.0
