import os

# Suffix conventions
LEVELED_SUFFIX = "_leveled"
THUMB_SUFFIX = "_leveled_thumb"

IMAGE_EXTS = set([".jpg", ".jpeg", ".png", ".webp", ".gif"])


def is_image_file(name):
    """
    Check whether a filename has an image extension supported by the tool.

    Parameters
    ----------
    name : str
        File name to check.

    Returns
    -------
    bool
        True if the extension is one of {".jpg", ".jpeg", ".png", ".webp", ".gif"}.
    """
    root, ext = os.path.splitext(name)
    return ext.lower() in IMAGE_EXTS


def is_thumb_name(name):
    """
    Determine whether a filename corresponds to a thumbnail.

    A thumbnail is identified by the logical base name ending with
    THUMB_SUFFIX ("_leveled_thumb").

    Parameters
    ----------
    name : str
        File name to check.

    Returns
    -------
    bool
        True if the name is recognized as a thumbnail file.
    """
    root, ext = os.path.splitext(name)
    return root.endswith(THUMB_SUFFIX)


def is_leveled_name(name):
    """
    Determine whether a filename is marked as a leveled image.

    A leveled image name ends with LEVELED_SUFFIX ("_leveled") before the
    file extension.

    Parameters
    ----------
    name : str
        File name to check.

    Returns
    -------
    bool
        True if the file name is recognized as a leveled image.
    """
    root, ext = os.path.splitext(name)
    return root.endswith(LEVELED_SUFFIX)


def logical_base_from_name(name):
    """
    Compute the logical base name for a file by stripping known suffixes.

    The following suffixes are removed in order: THUMB_SUFFIX ("_leveled_thumb"),
    legacy "_thumb", and LEVELED_SUFFIX ("_leveled"). The file extension is
    ignored when computing the base name.

    Parameters
    ----------
    name : str
        Input file name.

    Returns
    -------
    str
        The logical base name without thumbnail or leveled suffixes.
    """
    root, ext = os.path.splitext(name)
    base = root

    if base.endswith(THUMB_SUFFIX):
        base = base[:-len(THUMB_SUFFIX)]
    elif base.endswith("_thumb"):
        base = base[:-len("_thumb")]

    if base.endswith(LEVELED_SUFFIX):
        base = base[:-len(LEVELED_SUFFIX)]

    return base


def make_leveled_name(name):
    """
    Create the leveled variant of a given filename.

    Parameters
    ----------
    name : str
        Original file name including extension.

    Returns
    -------
    str
        File name with LEVELED_SUFFIX ("_leveled") inserted before the
        original extension.
    """
    root, ext = os.path.splitext(name)
    return root + LEVELED_SUFFIX + ext


def make_thumb_name_for_base(base, ext):
    """
    Create the thumbnail filename for a given logical base and extension.

    Parameters
    ----------
    base : str
        Logical base name (without suffixes and without extension).
    ext : str
        File extension to use for the thumbnail (including leading dot),
        usually derived from the source image.

    Returns
    -------
    str
        Thumbnail file name as base + THUMB_SUFFIX + ext.
    """
    return base + THUMB_SUFFIX + ext
