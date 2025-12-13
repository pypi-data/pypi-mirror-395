import os
import sys
import shutil
import argparse

from plumb.king.fs_scanner import discover_images
from plumb.king.naming import (
    make_leveled_name,
    logical_base_from_name,
)
from plumb.king.exif_utils import load_image_exif_corrected
from plumb.king.leveling_apply import level_image_final
from plumb.king.thumbnails import plan_thumbnails, create_thumbnail


def main():
    """
    Entry point for the command-line interface.

    Scans a directory for images, proposes leveling (horizon/roll correction),
    and generates missing thumbnails. If not in dry-run mode, it creates preview
    leveled images, asks for confirmation, applies replacements, and then creates
    thumbnails for leveled images as needed.

    Environment variables
    ---------------------
    LEVELED_PREVIEW_DIR : str, optional
        Name of the temporary preview directory created inside the target
        directory to store preview leveled images. Defaults to "_leveled_preview".
    THUMB_MAX_SIZE : int, optional
        Maximum size (in pixels) of the longer thumbnail edge. Defaults to 720.
    LEVEL_ANALYSIS_SIZE : int, optional
        Analysis size (in pixels) used internally by the leveling algorithm.

    Returns
    -------
    int
        Zero on success, non-zero on failure (e.g., when the given directory
        does not exist).
    """
    parser = argparse.ArgumentParser(description="Level images and generate thumbnails.")
    parser.add_argument("-d", "--directory", required=True)
    parser.add_argument("--dry-run", action="store_true")
    # NEW: optional debug directory for intermediate artifacts
    parser.add_argument(
        "--debug-dir",
        help=(
            "If set, write leveling debug intermediates "
            "(segmentation, edges, Hough overlays) into this directory."
        ),
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        print("Not a directory:", directory)
        return 1

    # Normalize debug_dir (can be None)
    debug_root = None
    if args.debug_dir:
        debug_root = os.path.abspath(args.debug_dir)
        os.makedirs(debug_root, exist_ok=True)

    print("Scanning:", directory)

    candidates, leveled, thumbs, others = discover_images(directory)

    print("\nImage classification:")
    print("  Candidates :", len(candidates))
    print("  Leveled    :", len(leveled))
    print("  Thumbs     :", len(thumbs))

    to_level = list(candidates)
    all_non_thumb = leveled + candidates

    thumb_ops = plan_thumbnails(directory, all_non_thumb, thumbs)

    print("\nPlan (leveling):")
    for name in to_level:
        print(" ", name, "->", make_leveled_name(name))

    print("\nPlan (thumbnails):")
    for src, dst in thumb_ops:
        print(" ", os.path.basename(src), "->", os.path.basename(dst))

    if args.dry_run:
        print("\nDry-run; no changes made.")
        return 0
    approved = False
    if to_level:
        preview_dir_name = os.environ.get("LEVELED_PREVIEW_DIR", "_leveled_preview")
        preview_path = os.path.join(directory, preview_dir_name)

        if os.path.exists(preview_path):
            if os.path.isdir(preview_path):
                shutil.rmtree(preview_path)
            else:
                os.remove(preview_path)

        os.makedirs(preview_path)

        print("\nGenerating preview leveled images:")
        for name in to_level:
            src = os.path.join(directory, name)
            out = os.path.join(preview_path, make_leveled_name(name))

            try:
                img = load_image_exif_corrected(src)

                # Per-image debug tag = logical base (no suffixes, no extension)
                debug_tag = logical_base_from_name(name)

                # If debug_root is provided, create a subfolder per image base
                if debug_root is not None:
                    dbg_dir = os.path.join(debug_root, debug_tag)
                    os.makedirs(dbg_dir, exist_ok=True)
                else:
                    dbg_dir = None

                final = level_image_final(
                    img,
                    debug_dir=dbg_dir,
                    debug_tag=debug_tag,
                )
                final.save(out, optimize=True)
                print("  PREVIEW:", name)
            except Exception as e:
                print("  ERROR:", name, e)

        print("\nReview previews at:", preview_path)
        try:
            ans = raw_input("Approve replacements? [y/N] ").strip().lower()
        except NameError:
            ans = input("Approve replacements? [y/N] ").strip().lower()

        if ans in ("y", "yes"):
            ans=True
            print("\nApplying leveled images...")
            for name in to_level:
                orig = os.path.join(directory, name)
                prev = os.path.join(preview_path, make_leveled_name(name))
                final = os.path.join(directory, make_leveled_name(name))

                if os.path.exists(prev):
                    shutil.move(prev, final)
                    if os.path.exists(orig):
                        os.remove(orig)
                        print("  REPLACED:", name)
                else:
                    print("  SKIP:", name)

            shutil.rmtree(preview_path, True)
        else:
            print("\nRollback.")
            shutil.rmtree(preview_path, True)

    # Refresh after leveling
    if approved:
        c2, l2, t2, _ = discover_images(directory)
        ops2 = plan_thumbnails(directory, l2 + c2, t2)

        if ops2:
            max_size = 720
            try:
                max_size = int(os.environ.get("THUMB_MAX_SIZE", "720"))
            except Exception:
                pass

            print("\nCreating thumbnails ({}px max):".format(max_size))
            for src, dst in ops2:
                try:
                    create_thumbnail(src, dst, max_size)
                except Exception as e:
                    print("  ERROR:", os.path.basename(dst), e)
    else:
        print("\nNo thumbnails needed.")

    return 0
