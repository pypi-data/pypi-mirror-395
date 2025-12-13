from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from nercone_modern.logging import ModernLogging

from .copy import copy_raw, detect_media_size, parse_size, verify_integrity


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Bit-exact, metadata-preserving copy utility for disks, images, partitions, or volumes."
        )
    )
    parser.add_argument("source", help="Path to the source block device, image, or file")
    parser.add_argument("destination", help="Path to the destination device, image, or file")
    parser.add_argument(
        "-b",
        "--block-size",
        default="4M",
        help="Block size for I/O (e.g. 1M, 4M, 1G). Default: 4M",
    )
    parser.add_argument(
        "--size",
        help="Explicit size to copy (bytes or human suffix). Overrides automatic detection.",
    )
    parser.add_argument(
        "--hash",
        default="sha256",
        help="Hash algorithm for integrity verification (default: sha256)",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip post-copy integrity verification (not recommended)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting an existing destination regular file.",
    )
    parser.add_argument(
        "--no-flush",
        action="store_true",
        help="Do not fsync the destination after writing (faster, less safe)",
    )
    parser.add_argument(
        "--process-name",
        default="nercone-fullcopy",
        help="Name used in the nercone-modern log output",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        block_size = parse_size(args.block_size)
    except ValueError:
        parser.error("Invalid block size format")
    declared_size = None
    if args.size:
        try:
            declared_size = parse_size(args.size)
        except ValueError:
            parser.error("Invalid size format")

    logger = ModernLogging(process_name=args.process_name)

    if os.path.exists(args.destination) and os.path.samefile(args.source, args.destination):
        logger.log("Source and destination are the same", level_text="ERROR", level_color="red")
        return 1

    logger.log(f"Preparing to clone {args.source} -> {args.destination}")
    detected_size = detect_media_size(args.source, logger)
    chosen_size = declared_size if declared_size is not None else detected_size
    if chosen_size:
        logger.log(f"Copy size: {chosen_size} bytes")
    else:
        logger.log("Size unknown. Using streaming copy with spinner progress.", level_text="WARN")

    try:
        copy_raw(
            source=args.source,
            destination=args.destination,
            logger=logger,
            block_size=block_size,
            declared_size=declared_size,
            force=args.force,
            flush=not args.no_flush,
        )
    except RuntimeError as exc:
        logger.log(str(exc), level_text="ERROR", level_color="red")
        return 1

    if args.skip_verify:
        logger.log(
            "Integrity verification was skipped at user request.", level_text="WARN", level_color="yellow"
        )
        return 0

    ok = verify_integrity(
        source=args.source,
        destination=args.destination,
        logger=logger,
        block_size=block_size,
        algo=args.hash,
        declared_size=chosen_size,
    )
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
