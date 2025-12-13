import os
import numpy as np
from PIL import Image
from plumb.king.exif_utils import normalize_mode
from plumb.king.leveling_core import (
    estimate_roll_multiscale_kmeans,
    to_canny,
    to_hough_lines,
    line_angles_and_lengths,
    epsilon_find_weighted,
)


def rotate_and_crop(img, phi_star):
    """
    Rotate an image by the given roll angle and crop to the largest inscribed rectangle.

    The image is rotated about its center by -phi_star (so that a positive
    phi_star would counter-rotate a positively rolled horizon), and then cropped
    to remove black borders, keeping the maximal axis-aligned rectangle fully
    inside the rotated image.

    Parameters
    ----------
    img : PIL.Image.Image
        Source image to rotate and crop.
    phi_star : float
        Roll angle in radians. Positive values indicate counter-clockwise roll
        to be corrected.

    Returns
    -------
    PIL.Image.Image
        The rotated and cropped image.
    """
    phi_deg = np.degrees(phi_star)
    rotated = img.rotate(-phi_deg, Image.BICUBIC, expand=False)

    W, H = rotated.size
    eps = abs(phi_star)

    w_inner = W * np.cos(eps) - H * np.sin(eps)
    h_inner = H * np.cos(eps) - W * np.sin(eps)
    w_inner = max(0.0, w_inner)
    h_inner = max(0.0, h_inner)

    left = (W - w_inner) / 2.0
    top = (H - h_inner) / 2.0
    right = left + w_inner
    bottom = top + h_inner

    crop_box = (
        int(round(left)),
        int(round(top)),
        int(round(right)),
        int(round(bottom)),
    )

    return rotated.crop(crop_box)


import os
import numpy as np
from PIL import Image

from plumb.king.exif_utils import normalize_mode
from plumb.king.leveling_core import (
    estimate_roll_multiscale_kmeans,
    to_canny,
    to_hough_lines,
    line_angles_and_lengths,
    epsilon_find_weighted,
)

PLUMB_DEBUG = os.environ.get("PLUMB_DEBUG", "0") == "1"


def to_gray(img: Image.Image) -> Image.Image:
    return img.convert("L")


def refine_roll_joint(
        angles: np.ndarray,
        lengths: np.ndarray,
        phi_initial: float,
        search_deg: float = 3.0,
        steps: int = 13,
) -> float:
    """
    Refine an initial roll estimate phi_initial by choosing the phi in a small
    neighborhood that best aligns lines to *either* 0° (horizontal)
    *or* 90° (vertical), weighted by length.

    angles: line angles in radians, normalized to [-pi/2, pi/2)
    lengths: line lengths
    phi_initial: starting roll angle in radians
    """
    if angles.size == 0 or lengths.size == 0:
        return phi_initial

    A = angles.astype(float)
    L = lengths.astype(float)
    Lmax = L.max()
    if Lmax <= 0:
        return phi_initial

    # length-based weights
    w = L / (Lmax + 1e-6)

    delta = np.radians(search_deg)
    phi_candidates = np.linspace(phi_initial - delta, phi_initial + delta, steps)

    best_phi = phi_initial
    best_score = float("inf")

    for phi in phi_candidates:
        # rotate angles by phi
        Ar = A + phi
        # wrap to [-pi/2, pi/2)
        Ar = (Ar + np.pi / 2.0) % np.pi - np.pi / 2.0

        # distance to 0° (horizontal)
        dist_h = Ar  # radians

        # distance to ±90° (vertical)
        dist_v = np.abs(Ar) - np.pi / 2.0
        dist_v = np.where(dist_v < 0, -dist_v, dist_v)  # abs

        # nearest axis (horizontal or vertical)
        d2 = np.minimum(dist_h ** 2, dist_v ** 2)

        score = float(np.sum(w * d2))
        if score < best_score:
            best_score = score
            best_phi = phi

    return best_phi


def compute_leveling_angle_from_thumbnail(
        img: Image.Image,
        analysis_size: int = 720,
        max_correction_deg: float = 35.0,
        crop_top: float = 0.20,
        crop_bottom: float = 0.20,
        crop_left: float = 0.15,
        crop_right: float = 0.15,
        debug_dir: str | None = None,
        debug_tag: str = "",
) -> float:
    """
    Compute a leveling angle (in radians) using a cropped thumbnail of the image.

    Cropping parameters are fractional (0.0 → keep, 1.0 → remove entire side).

    Steps:
      1) Downscale to analysis_size.
      2) Apply fractional crop (top/bottom/left/right).
      3) Run multiscale k-means + Hough voting on cropped region.
      4) Fallback to single-pass Canny+Hough if multiscale has no opinion.
      5) Refine around the chosen angle using joint horiz/vert alignment.
      6) Discard extreme corrections.
    """

    # 1) Create thumbnail for analysis
    thumb = img.copy()
    thumb.thumbnail((analysis_size, analysis_size), resample=Image.BICUBIC)
    tw, th = thumb.size

    if tw < 10 or th < 10:
        return 0.0

    # 2) Fractional cropping
    crop_top = max(0.0, min(0.9, crop_top))
    crop_bottom = max(0.0, min(0.9, crop_bottom))
    crop_left = max(0.0, min(0.9, crop_left))
    crop_right = max(0.0, min(0.9, crop_right))

    left_px = int(tw * crop_left)
    right_px = int(tw * (1.0 - crop_right))
    top_px = int(th * crop_top)
    bottom_px = int(th * (1.0 - crop_bottom))

    if right_px <= left_px or bottom_px <= top_px:
        return 0.0

    crop_img = thumb.crop((left_px, top_px, right_px, bottom_px))

    # --- Debug: save the analysis thumb + crop ---
    if debug_dir is not None:
        try:
            os.makedirs(debug_dir, exist_ok=True)
            base = debug_tag or "debug"

            # full thumbnail
            thumb_path = os.path.join(debug_dir, f"{base}_thumb_analysis.png")
            thumb.save(thumb_path)

            # cropped band used for leveling
            crop_path = os.path.join(debug_dir, f"{base}_crop.png")
            crop_img.save(crop_path)
        except Exception:
            pass

    # 3) Multiscale k-means + Hough voting
    phi_star = estimate_roll_multiscale_kmeans(
        crop_img,
        max_correction_deg=max_correction_deg,
        debug_dir=debug_dir,
        debug_tag=debug_tag,
    )

    # 4) Fallback: original single-pass Canny + Hough + epsilon_find_weighted
    if abs(phi_star) < 1e-5:
        gray = to_gray(crop_img)
        edges = to_canny(gray)
        lines = to_hough_lines(edges)

        if lines.shape[0] == 0:
            return 0.0

        angles, lengths = line_angles_and_lengths(lines)
        mean_sin, mean_cos = epsilon_find_weighted(
            angles,
            lengths,
            p=1.1,
            max_angle_deg=max_correction_deg,
        )
        phi_star = float(np.arctan2(mean_sin, mean_cos))

    # 4b) Joint horizontal + vertical refinement around phi_star
    try:
        gray_ref = to_gray(crop_img)
        edges_ref = to_canny(gray_ref)
        lines_ref = to_hough_lines(edges_ref)
        if lines_ref.shape[0] > 0:
            angles_ref, lengths_ref = line_angles_and_lengths(lines_ref)
            phi_star = refine_roll_joint(angles_ref, lengths_ref, phi_star)
    except Exception:
        # refinement is best-effort; never break the pipeline
        pass

    max_rad = np.radians(max_correction_deg)
    if abs(phi_star) > max_rad:
        return 0.0

    return phi_star


def level_image_final(
        img: Image.Image,
        debug_dir: str | None = None,
        debug_tag: str = "",
) -> Image.Image:
    """
    Apply leveling using a thumbnail-derived angle.

    - Reads LEVEL_ANALYSIS_SIZE from env (default 720).
    - Uses compute_leveling_angle_from_thumbnail(...) to estimate roll.
    - If angle is tiny, returns a copy.
    - Otherwise rotates, crops, and resizes back to original size.
    """
    W, H = img.size

    # 1) Determine analysis size from env
    analysis_size_str = os.environ.get("LEVEL_ANALYSIS_SIZE", "720")
    try:
        analysis_size = int(analysis_size_str)
    except ValueError:
        analysis_size = 720

    # 2) Compute roll angle from a cropped thumbnail
    phi_star = compute_leveling_angle_from_thumbnail(
        img,
        analysis_size=analysis_size,
        max_correction_deg=35.0,
        debug_dir=debug_dir,
        debug_tag=debug_tag,
    )

    # Debug: print angle in degrees (gate with an env if you want to mute it)
    print(f"[DEBUG] phi_star (deg) = {np.degrees(phi_star):.3f}")

    # If no meaningful correction, just return a copy
    if abs(phi_star) < 1e-5:
        return img.copy()

    # 3) Rotate & crop full-res with the same angle
    cropped = rotate_and_crop(img, phi_star)

    # 4) Resize cropped back to original resolution
    final = cropped.resize((W, H), resample=Image.BICUBIC)
    return final
