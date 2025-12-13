import os
from typing import Tuple, List

import numpy as np
import cv2
from PIL import Image
from itertools import count
from plumb.king.exif_utils import normalize_mode

# from plumb.king.leveling_apply import to_gray

# ------------------------------
# Debug helpers
# ------------------------------

PLUMB_DEBUG = os.environ.get("PLUMB_DEBUG", "0") == "1"
PLUMB_DEBUG_DIR = os.environ.get("PLUMB_DEBUG_DIR", "_leveled_debug")

if PLUMB_DEBUG:
    os.makedirs(PLUMB_DEBUG_DIR, exist_ok=True)

_debug_counter = count()


def to_gray(img: Image.Image) -> Image.Image:
    return img.convert("L")


def debug_save_image(label: str, img_or_arr):
    """
    Save a debug image into PLUMB_DEBUG_DIR with an incrementing prefix.

    Accepts either a PIL.Image or a numpy array (H,W) or (H,W,3).
    Does nothing if PLUMB_DEBUG is False.
    """
    if not PLUMB_DEBUG:
        return

    idx = next(_debug_counter)
    filename = f"{idx:03d}_{label}.png"
    path = os.path.join(PLUMB_DEBUG_DIR, filename)

    if isinstance(img_or_arr, Image.Image):
        img = img_or_arr
    else:
        arr = np.asarray(img_or_arr)
        if arr.ndim == 2:
            img = Image.fromarray(arr.astype(np.uint8), mode="L")
        elif arr.ndim == 3:
            # assume RGB/BGR-ish, convert to RGB if needed
            if arr.shape[2] == 3:
                img = Image.fromarray(arr.astype(np.uint8))
            else:
                # fallback: take first 3 channels
                img = Image.fromarray(arr[..., :3].astype(np.uint8))
        else:
            # unsupported shape; bail out
            return

    try:
        img.save(path)
    except Exception:
        # debug only; ignore failures
        pass


# ------------------------------
# K-means segmentation
# ------------------------------

def kmeans_segment_gray(img, k, pre_blur_ksize, rng_seed):
    """
    Segment an RGB image into k gray-ish regions using OpenCV k-means.

    The input PIL image is converted to RGB, optionally pre-blurred, then
    clustered in color space. The resulting labels are mapped to a grayscale
    palette evenly spanning [0, 255].

    Parameters
    ----------
    img : PIL.Image.Image
        Input image.
    k : int
        Number of clusters for k-means. If k <= 1, a zero mask is returned.
    pre_blur_ksize : int
        Optional Gaussian blur kernel size (pixels). If even and > 0, it will
        be incremented to the next odd value as required by OpenCV.
    rng_seed : int
        Random seed placeholder (not used directly; OpenCV uses its own init).

    Returns
    -------
    numpy.ndarray
        A 2D uint8 array of shape (H, W) containing k distinct gray values.
    """
    rgb = np.array(img.convert("RGB"), dtype=np.uint8)
    h, w, _ = rgb.shape

    if pre_blur_ksize and pre_blur_ksize > 1:
        if pre_blur_ksize % 2 == 0:
            pre_blur_ksize += 1
        rgb = cv2.GaussianBlur(rgb, (pre_blur_ksize, pre_blur_ksize), 0)

    samples = rgb.reshape(-1, 3).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    attempts = 3
    flags = cv2.KMEANS_PP_CENTERS

    compactness, labels, centers = cv2.kmeans(
        samples, k, None, criteria, attempts, flags
    )

    labels = labels.reshape(h, w)

    if k <= 1:
        seg = np.zeros((h, w), dtype=np.uint8)
        debug_save_image("kmeans_seg_k1", seg)
        return seg

    step = 255 // (k - 1)
    palette = np.arange(k, dtype=np.uint8) * step
    seg = palette[labels]

    debug_save_image(f"kmeans_seg_k{k}", seg)
    return seg


# ------------------------------
# Canny + Variance mask
# ------------------------------
def variance_mask(arr: np.ndarray, ksize: int = 35, quantile: float = 0.80) -> np.ndarray:
    """
    Compute local variance and mask OUT the highest-variance regions.
    These usually correspond to water ripples, noisy grass, textured floors, etc.
    """
    arr_f = arr.astype(np.float32)
    mean = cv2.blur(arr_f, (ksize, ksize))
    mean2 = cv2.blur(arr_f * arr_f, (ksize, ksize))
    var = mean2 - mean * mean

    thresh = np.quantile(var, quantile)
    return var <= thresh


def to_canny(
        gray_img: Image.Image,
        blur_ksize: int = 10,
        low_thresh: int = 15,
        high_thresh: int = 50,
        use_variance_mask: bool = False,
) -> np.ndarray:
    """
    Canny on a heavily low-passed image:
      - Large Gaussian blur (kills high-frequency texture)
      - Optional variance mask to remove very noisy regions
    """
    arr = np.array(gray_img, dtype=np.uint8)

    # --- Low-pass via Gaussian blur ---
    if blur_ksize % 2 == 0:
        blur_ksize += 1
    arr_blur = cv2.GaussianBlur(arr, (blur_ksize, blur_ksize), 0)

    edges = cv2.Canny(arr_blur, low_thresh, high_thresh)

    # --- Optional: remove high-variance regions ---
    if use_variance_mask:
        mask = variance_mask(arr_blur, ksize=blur_ksize, quantile=0.80)
        edges[~mask] = 0

    return edges


# ------------------------------
# Hough + Angle aggregation
# ------------------------------

def to_hough_lines(edges):
    """
    Run probabilistic Hough transform to extract line segments from an edge map.

    Parameters
    ----------
    edges : numpy.ndarray
        Binary edge image (uint8) as returned by Canny, shape (H, W).

    Returns
    -------
    numpy.ndarray
        Array of shape (N, 4) with line segments in (x1, y1, x2, y2) format.
        Returns an empty array with shape (0, 4) if no lines are detected.
    """
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180.0,
        80,
        minLineLength=50,
        maxLineGap=10,
    )
    if lines is None:
        return np.empty((0, 4), dtype=np.float32)
    lines_arr = lines.reshape(-1, 4)

    # debug overlay: draw lines on top of edges
    if PLUMB_DEBUG and edges.size > 0 and lines_arr.size > 0:
        overlay = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        for (x1, y1, x2, y2) in lines_arr:
            cv2.line(overlay, (x1, y1), (x2, y2), (0, 255, 0), 1)
        debug_save_image("hough_lines_overlay", overlay)

    return lines_arr


def line_angles_and_lengths(lines):
    """
    Compute line segment orientations and lengths.

    Parameters
    ----------
    lines : numpy.ndarray
        Array of shape (N, 4) with segments in (x1, y1, x2, y2) format.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        A tuple (theta, lengths) where theta are angles in radians normalized
        to [-pi/2, pi/2), and lengths are segment lengths in pixels.
    """
    xs = lines[:, 2] - lines[:, 0]
    ys = lines[:, 3] - lines[:, 1]
    theta = np.arctan2(ys, xs)
    theta = (theta + np.pi / 2) % np.pi - np.pi / 2
    lengths = np.hypot(xs, ys)
    return theta, lengths


def estimate_roll_horizon_ransac(
        seg_gray: np.ndarray,
        max_angle_deg: float = 35.0
) -> tuple[float, float]:
    """
    Coarse horizon detector.

    Returns:
        (phi_radians, confidence_in_[0,1])
    If detection fails:
        (0.0, 0.0)

    Notes:
    - Uses Otsu threshold to separate sky/water bands.
    - Finds the LAST bright pixel per column as the sky boundary.
    - Fits a line with RANSAC; slope -> roll.
    - Confidence = inlier ratio.
    - sklearn is optional; if unavailable, returns (0,0).
    """

    h, w = seg_gray.shape

    # sklearn availability check
    try:
        from sklearn.linear_model import RANSACRegressor, LinearRegression
    except Exception:
        return 0.0, 0.0

    # --- 1) Otsu threshold to get sky-ish mask ---
    # Assumes sky is brighter in segmented grayscale.
    try:
        _, sky_mask = cv2.threshold(
            seg_gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    except Exception:
        return 0.0, 0.0

    # --- 2) Find sky boundary per column ---
    xs, ys = [], []
    for x in range(w):
        col = sky_mask[:, x]
        idx = np.where(col > 0)[0]
        if idx.size == 0:
            continue
        ys.append(idx[-1])  # last bright pixel (bottom of sky)
        xs.append(x)

    if len(xs) < 10:
        return 0.0, 0.0

    # prepare regression variables
    X = np.asarray(xs, dtype=np.float32).reshape(-1, 1)
    y = np.asarray(ys, dtype=np.float32)

    # --- 3) RANSAC line fit ---
    try:
        ransac = RANSACRegressor(
            estimator=LinearRegression(),
            min_samples=0.5,  # 50% inliers
            residual_threshold=3.0,  # vertical tolerance (pixels)
            max_trials=200,
            random_state=0,
        )
        ransac.fit(X, y)
    except Exception:
        return 0.0, 0.0

    inlier_mask = ransac.inlier_mask_
    if inlier_mask is None or not np.any(inlier_mask):
        return 0.0, 0.0

    # slope m -> roll angle
    try:
        m = float(ransac.estimator_.coef_[0])
    except Exception:
        return 0.0, 0.0

    phi = -np.arctan(m)

    # reject implausible angles
    if abs(phi) > np.radians(max_angle_deg):
        return 0.0, 0.0

    # confidence = inlier ratio
    conf = float(np.mean(inlier_mask))

    return phi, conf


def epsilon_find_weighted(
        angles: np.ndarray,
        lengths: np.ndarray,
        p: float = 4.0,
        top_fraction: float = 1.0,
        axis_thresh: float = 0.90,  # kept for compat, not used
        max_angle_deg: float = 35.0,  # max allowed roll correction
        bin_size_deg: float = 10.0,  # histogram resolution
        cluster_halfwidth_deg: float = 3.0,
        dominance_ratio: float = 1.0,  # if best vs second is weak, prefer smaller |roll|
        min_total_length: float = 0.1,  # cluster must have substantial evidence
) -> Tuple[float, float]:
    """
    Roll / horizon estimator using:
      • length-dominated weighting (axis weighting is effectively neutral)
      • longest lines only (via top_fraction)
      • 1D clustering in roll (φ) space

    If the top two histogram bins are not dominant enough over each other,
    we keep the one whose roll center is closer to 0° (smaller |φ|),
    instead of giving up.

    Returns (mean_sin, mean_cos) for the roll angle.
    """

    if angles.size == 0 or lengths.size == 0:
        return 0.0, 1.0

    A = angles.astype(float)
    L = lengths.astype(float)

    Lmax_global = L.max()
    if Lmax_global <= 0:
        return 0.0, 1.0

    # ----------------------------
    # 1) Longest top_fraction lines
    # ----------------------------
    N = L.size
    k = max(1, int(np.ceil(N * top_fraction)))
    idx = np.argsort(L)[-k:]
    A = A[idx]
    L = L[idx]

    if A.size == 0:
        return 0.0, 1.0

    # ----------------------------
    # 2) Convert to roll votes φ with (almost neutral) axis weighting
    # ----------------------------
    # axis weight in θ-space – effectively ~1, kept for future tweaks
    axis_w = (np.cos(A / 999.0) ** 2) ** 0.5  # in [~1, ~1]

    theta_deg = np.degrees(A)
    axes = np.array([0.0, 90.0, -90.0], dtype=float)  # horiz, vert, vert

    # nearest axis for each line
    diff = axes[:, None] - theta_deg[None, :]
    dist = np.abs(diff)
    nearest_idx = np.argmin(dist, axis=0)
    nearest_axis_deg = axes[nearest_idx]
    axis_dist_deg = dist[nearest_idx, np.arange(dist.shape[1])]

    # roll vote: φ = axis - θ  (how much to rotate to make this line axis-aligned)
    roll_deg = nearest_axis_deg - theta_deg

    # heuristics: line must be reasonably axis-ish & roll must be plausible
    axis_tolerance_deg = 35.0
    mask = (
            (axis_dist_deg <= axis_tolerance_deg) &
            (np.abs(roll_deg) <= max_angle_deg)
    )

    if not np.any(mask):
        return 0.0, 1.0

    roll_deg = roll_deg[mask]
    L = L[mask]
    axis_w = axis_w[mask]

    # combined weight: length^p * axis_w
    Lmax = L.max()
    if Lmax <= 0:
        return 0.0, 1.0
    Lnorm = (L / Lmax) ** p
    w = Lnorm * axis_w

    keep = w > 0
    if not np.any(keep):
        return 0.0, 1.0

    roll_deg = roll_deg[keep]
    w = w[keep]

    # ----------------------------
    # 3) Histogram clusters in roll-space
    # ----------------------------
    bin_edges = np.arange(-max_angle_deg, max_angle_deg + bin_size_deg, bin_size_deg)
    hist, _ = np.histogram(roll_deg, bins=bin_edges, weights=w)
    if hist.sum() == 0:
        return 0.0, 1.0

    # sort bins by weight to get top-1 and top-2 indices
    order = np.argsort(hist)
    best_idx = order[-1]
    best_val = hist[best_idx]

    if hist.size >= 2:
        second_idx = order[-2]
        second_val = hist[second_idx]
    else:
        second_idx = None
        second_val = 0.0

    if best_val < min_total_length:
        return 0.0, 1.0

    centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # If dominance is weak, pick whichever of the top two
    # clusters corresponds to the smaller |roll| (closer to level).
    cluster_idx = best_idx
    if second_idx is not None and second_val > 0:
        ratio = best_val / max(second_val, 1e-8)
        if ratio < dominance_ratio:
            candidate_indices = [best_idx, second_idx]
            cluster_idx = min(candidate_indices, key=lambda i: abs(centers[i]))

    # ----------------------------
    # 4) Mean roll angle within chosen cluster window
    # ----------------------------
    best_center = centers[cluster_idx]

    mask_cluster = np.abs(roll_deg - best_center) <= cluster_halfwidth_deg
    if not np.any(mask_cluster):
        return 0.0, 1.0

    phi_cluster_rad = np.radians(roll_deg[mask_cluster])
    wcluster = w[mask_cluster]
    w_sum = wcluster.sum()
    if w_sum <= 0:
        return 0.0, 1.0

    mean_sin = float(np.sum(wcluster * np.sin(phi_cluster_rad)) / w_sum)
    mean_cos = float(np.sum(wcluster * np.cos(phi_cluster_rad)) / w_sum)

    return mean_sin, mean_cos


# ----------------------------------------------------------
# Multiscale angle estimation
# ----------------------------------------------------------

def estimate_roll_multiscale_kmeans(
        crop_img: Image.Image,
        max_correction_deg: float = 25.0,
        debug_dir: str | None = None,
        debug_tag: str = "",
) -> float:
    """
    Run several k-means + edge + Hough passes at different
    effective resolutions and combine their roll estimates.

    Coarser passes (heavier blur, lower scale) get larger votes.
    """
    crop_w, crop_h = crop_img.size

    # (k, pre_blur_ksize, scale_factor, pass_weight)
    configs = [
        # detail-ish
        # (64, 14, 1.00, 1.0),
        (32, 12, 0.50, 4.0),
        # mid-scale
        (16, 10, 0.25, 9.0),
        # coarse, only big structures survive
        (8, 8, 0.12, 16.0),
        (4, 6, 0.08, 25.0),
        (2, 4, 0.05, 36.0),
    ]

    phi_list: List[float] = []
    w_list: List[float] = []

    def _hough_lines_scaled(edges: np.ndarray) -> np.ndarray:
        """
        Probabilistic Hough with progressive relaxation.
        Start strict; if we don't get enough lines, allow shorter segments.
        """
        h, w = edges.shape[:2]

        # (min_len_frac, gap_frac, threshold)

        attempts = [
            (0.30, 0.0001, 5000),
            (0.15, 0.001, 500),
            (0.05, 0.25, 50),
            (0.01, 1.0, 3),
        ]
        best_lines = np.zeros((0, 4), dtype=np.int32)

        for min_frac, gap_frac, thr in attempts:
            min_line_len = max(6, int(min_frac * w))
            max_line_gap = max(2, int(gap_frac * w))

            lines = cv2.HoughLinesP(
                edges,
                rho=1.0,
                theta=np.pi / 180.0,
                threshold=thr,
                minLineLength=min_line_len,
                maxLineGap=max_line_gap,
            )
            if lines is None:
                continue

            lines = lines.reshape(-1, 4)
            best_lines = lines

            # if we already have "enough" segments, stop relaxing
            if lines.shape[0] >= 20:
                break

        return best_lines

    for (k, pre_blur, scale, pass_weight) in configs:
        pass_id = f"k{k}_b{pre_blur}_s{scale:.2f}"

        # Build a scaled version of the crop for this pass
        scaled_img = crop_img
        if 0.0 < scale < 1.0:
            w, h = crop_img.size
            sw = max(8, int(w * scale))
            sh = max(8, int(h * scale))
            scaled_img = crop_img.resize((sw, sh), resample=Image.BICUBIC)

        try:
            seg_gray_small = kmeans_segment_gray(
                scaled_img,
                k=k,
                pre_blur_ksize=pre_blur,
                rng_seed=1234,
            )
        except Exception:
            # If k-means fails on a weird crop, skip this pass
            continue

        # 2) Scale segmentation back up to crop size for geometry
        seg_gray = cv2.resize(
            seg_gray_small,
            (crop_w, crop_h),
            interpolation=cv2.INTER_NEAREST,  # preserve superpixel borders
        )
        h_seg, w_seg = seg_gray.shape[:2]

        # --- Anti-alias + (optional) unsharp mask BEFORE Canny/Hough ---
        # Light Gaussian smooth to kill stair-steps
        aa = cv2.GaussianBlur(seg_gray, (5, 5), 0)

        # Unsharp mask to keep edges defined but smooth
        sharp = cv2.addWeighted(seg_gray, 1.5, aa, -0.5, 0)
        edge_source = sharp
        # ----------------------------------------------------------------

        # Canny on anti-aliased edge source
        if scale > 0.50:
            # fine scale: normal Canny
            edges = cv2.Canny(seg_gray, 50, 150)
        else:
            # coarse: blur, then unsharp to keep big structures crisp
            s = max(scale, 0.05)
            sigma = min(24.0, 8.0 / s)
            ksize = max(3, int(6 * sigma) | 1)  # odd kernel, at least 3x3

            # 1) big blur to smooth the blocky superpixels
            blur = cv2.GaussianBlur(seg_gray, (ksize, ksize), sigmaX=sigma)

            # 2) unsharp mask: emphasize broad edges, suppress tiny jaggies
            amount = 1.0 if scale > 0.12 else 12.0
            seg_unsharp = cv2.addWeighted(seg_gray, 1.0 + amount, blur, -amount, 0)

            # 3) now run a softer Canny on the smoothed-but-crisp image
            edges = cv2.Canny(seg_unsharp, 15, 50)

        edge_count = int(np.count_nonzero(edges))

        # Use the scale-aware Hough instead of a generic one
        lines = _hough_lines_scaled(edges)
        if lines.shape[0] == 0:
            continue
        num_lines = int(lines.shape[0])

        # Cheap debug line
        print(
            f"[LEVEL] {pass_id}: seg={w_seg}x{h_seg} "
            f"edges={edge_count} lines={num_lines}"
        )

        # Optional debug overlay
        if debug_dir is not None:
            try:
                os.makedirs(debug_dir, exist_ok=True)
                base = debug_tag or "debug"
                tag = f"{base}_k{k}_b{pre_blur}_s{scale:.2f}"

                # segmented grayscale
                seg_path = os.path.join(debug_dir, f"{tag}_seg.png")
                Image.fromarray(seg_gray).save(seg_path)

                # anti-aliased / sharpened source
                aa_path = os.path.join(debug_dir, f"{tag}_aa.png")
                Image.fromarray(edge_source).save(aa_path)

                # canny edges
                edges_path = os.path.join(debug_dir, f"{tag}_canny.png")
                Image.fromarray(edges).save(edges_path)

                # hough overlay
                overlay = cv2.cvtColor(seg_gray, cv2.COLOR_GRAY2BGR)
                for x1, y1, x2, y2 in lines:
                    cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 1)
                hough_path = os.path.join(debug_dir, f"{tag}_hough.png")
                Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)).save(
                    hough_path
                )
            except Exception:
                # debugging should never break the pipeline
                pass

        # Feed into roll estimator
        angles, lengths = line_angles_and_lengths(lines)
        mean_sin, mean_cos = epsilon_find_weighted(
            angles,
            lengths,
            max_angle_deg=max_correction_deg,
        )

        phi = float(np.arctan2(mean_sin, mean_cos))
        if not np.isfinite(phi):
            continue

        if abs(phi) > np.radians(max_correction_deg):
            # This pass thinks it's crazy tilted; probably wrong
            continue

        phi_list.append(phi)
        w_list.append(pass_weight)

        # RANSAC horizon vote on coarse passes (e.g., two-band sky/water-ish)
        if k == 2:
            phi_r, conf_r = estimate_roll_horizon_ransac(
                seg_gray,
                max_angle_deg=max_correction_deg,
            )
            if conf_r > 0.0:
                phi_list.append(phi_r)
                # give RANSAC a strong, but not infinite, say
                w_list.append(pass_weight * (2.0 + 3.0 * conf_r))

    if not phi_list:
        return 0.0

    phis = np.array(phi_list, dtype=float)
    weights = np.array(w_list, dtype=float)

    # Weighted circular mean
    sin_sum = float(np.sum(weights * np.sin(phis)))
    cos_sum = float(np.sum(weights * np.cos(phis)))
    if sin_sum == 0.0 and cos_sum == 0.0:
        return 0.0

    phi_star = float(np.arctan2(sin_sum, cos_sum))

    # If no meaningful correction, fallback to a simpler pipeline
    if abs(phi_star) < 1e-2:
        gray = to_gray(crop_img)
        edges_fb = to_canny(gray)
        lines_fb = _hough_lines_scaled(edges_fb)

        if debug_dir is not None:
            try:
                base = debug_tag or "debug"
                edges_path = os.path.join(debug_dir, f"{base}_canny_fallback.png")
                Image.fromarray(edges_fb).save(edges_path)

                if lines_fb.shape[0] > 0:
                    overlay = cv2.cvtColor(np.array(gray), cv2.COLOR_GRAY2BGR)
                    for x1, y1, x2, y2 in lines_fb:
                        cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    hough_path = os.path.join(debug_dir, f"{base}_hough_fallback.png")
                    Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)).save(
                        hough_path
                    )
            except Exception:
                pass

        if lines_fb.shape[0] == 0:
            return 0.0

        # IMPORTANT: recompute mean_sin/mean_cos for fallback, not reuse old sums
        fb_angles, fb_lengths = line_angles_and_lengths(lines_fb)
        fb_sin, fb_cos = epsilon_find_weighted(
            fb_angles,
            fb_lengths,
            max_angle_deg=max_correction_deg,
        )
        phi_star = float(np.arctan2(fb_sin, fb_cos))
        return phi_star

    return phi_star
