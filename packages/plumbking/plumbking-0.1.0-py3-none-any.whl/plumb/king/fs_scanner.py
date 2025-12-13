import os
from plumb.king.naming import (
    is_image_file,
    is_thumb_name,
    is_leveled_name,
)


def discover_images(directory):
    """
    Discover and classify files in a directory related to image processing.

    Files are classified into four categories based on their names and
    extensions: candidate images (originals), already leveled images,
    thumbnails, and others (non-files or non-image files).

    Parameters
    ----------
    directory : str or path-like
        Path to the directory to scan.

    Returns
    -------
    tuple[list[str], list[str], list[str], list[str]]
        A 4-tuple containing:
        - candidates: image files eligible for leveling
        - leveled: files already marked as leveled
        - thumbs: thumbnail files
        - others: everything else (including subdirectories)
    """
    candidates = []
    leveled = []
    thumbs = []
    others = []

    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)

        if not os.path.isfile(full_path):
            others.append(entry)
            continue

        if is_thumb_name(entry):
            thumbs.append(entry)
        elif is_leveled_name(entry):
            leveled.append(entry)
        elif is_image_file(entry):
            candidates.append(entry)
        else:
            others.append(entry)

    return candidates, leveled, thumbs, others
