from PIL import Image, ImageOps


def load_image_exif_corrected(path):
    """
    Load an image from disk and apply EXIF-based orientation correction.

    Parameters
    ----------
    path : str or path-like
        Filesystem path to the source image.

    Returns
    -------
    PIL.Image.Image
        The opened image with EXIF orientation transposed to the correct
        viewing orientation when applicable.
    """
    img = Image.open(path)
    return ImageOps.exif_transpose(img)


def normalize_mode(img):
    """
    Ensure the image is in a processing-friendly color mode.

    Converts images that are not in "RGB" or grayscale ("L") to "RGB".

    Parameters
    ----------
    img : PIL.Image.Image
        Input image.

    Returns
    -------
    PIL.Image.Image
        The same image if already in mode "RGB" or "L"; otherwise a copy
        converted to "RGB".
    """
    m = img.mode
    if m not in ("RGB", "L"):
        return img.convert("RGB")
    return img
