import argparse
from pathlib import Path

from assi.datasets.mimii.storage import MIMIIStorage, DATASET_PARTS_ZIP_URLS

if __name__ == "__main__":
    # === parser definition ===
    parser = argparse.ArgumentParser(
        prog="MIMII downloader",
        description="Downloads MIMII dataset from zenodo",
    )

    parser.add_argument("basepath", type=Path, help="Directory to download")
    parser.add_argument(
        "-p",
        "--parts",
        nargs="+",
        choices=DATASET_PARTS_ZIP_URLS.keys(),
        help=f"List of parts (allowed: {', '.join(DATASET_PARTS_ZIP_URLS.keys())})",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Force the downloading"
    )

    # === args parsing ===
    args = parser.parse_args()
    dataset_base_folder = args.basepath
    part_names = args.parts
    if part_names is None:
        part_names = []
    force = args.force

    # === processing ===
    for part_name in part_names:
        MIMIIStorage(dataset_base_folder, part_name).check_integrity(force=force)
