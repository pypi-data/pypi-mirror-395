import os
from PIL import Image, ImageOps
from plumb.king.naming import (
    logical_base_from_name,
    make_thumb_name_for_base,
    is_thumb_name,
    is_leveled_name,
)


def plan_thumbnails(directory, images, existing_thumbs):
    """
    Plan thumbnail creation operations for a set of images.

    For each logical base and extension, prefer the leveled version if present
    among the inputs, skip any images that are already thumbnails, and avoid
    creating thumbnails that already exist.

    Parameters
    ----------
    directory : str or path-like
        Base directory that contains the images.
    images : list[str]
        Image file names to consider (relative to directory).
    existing_thumbs : list[str]
        Existing thumbnail file names (relative to directory).

    Returns
    -------
    list[tuple[str, str]]
        A list of (src_path, thumb_path) pairs describing the thumbnails to
        create.
    """
    thumb_keys = set()
    for t in existing_thumbs:
        base = logical_base_from_name(t)
        ext = os.path.splitext(t)[1].lower()
        thumb_keys.add((base, ext))

    canonical = {}

    for fname in images:
        if is_thumb_name(fname):
            continue

        base = logical_base_from_name(fname)
        _, ext = os.path.splitext(fname)
        ext = ext.lower()
        key = (base, ext)

        prev = canonical.get(key)
        if prev is None:
            canonical[key] = fname
        else:
            if is_leveled_name(fname) and not is_leveled_name(prev):
                canonical[key] = fname

    ops = []

    for (base, ext), src_name in canonical.items():
        key = (base, ext)
        if key in thumb_keys:
            continue

        src_path = os.path.join(directory, src_name)
        thumb_name = make_thumb_name_for_base(base, ext)
        thumb_path = os.path.join(directory, thumb_name)

        ops.append((src_path, thumb_path))
        thumb_keys.add(key)

    return ops


def create_thumbnail(src_path, thumb_path, max_size):
    """
    Create a thumbnail for the given image path and save it.

    The image is opened, EXIF orientation is applied, color mode is normalized
    to an RGB-friendly mode when necessary, and the image is resized to fit
    within max_size x max_size while preserving aspect ratio.

    Parameters
    ----------
    src_path : str or path-like
        Source image file path.
    thumb_path : str or path-like
        Destination file path for the thumbnail.
    max_size : int
        Maximum size in pixels for the longer edge of the thumbnail.

    Returns
    -------
    None
        This function has no return value; it saves the thumbnail to disk.
    """
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    img.thumbnail((max_size, max_size))
    img.save(thumb_path, optimize=True)
    print("  THUMB CREATED", os.path.basename(thumb_path))
