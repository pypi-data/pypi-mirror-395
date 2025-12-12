import os
import sys
from blake3 import blake3
from pathlib import Path
import logging

import argparse

logging.basicConfig(level=os.getenv("LOGGING_LEVEL", "INFO"))
logger = logging.getLogger("OICM_Checksum")


def hash_directory(path: Path) -> str:
    """Recursively hash a directory tree."""
    try:
        entries = sorted(os.scandir(path), key=lambda e: e.name)
        logger.info(f"entries: {entries}")
    except OSError as exc:
        logger.error(f"Unable to read directory {path}: {exc}")
        raise

    parts = []
    for entry in entries:
        if entry.name in {".", ".."}:
            continue
        entry_path = entry.path
        try:
            if entry.is_symlink():
                # Record symlink target
                target = Path(os.readlink(entry.path)).as_posix()
                parts.append(f"l:{entry.name}:{target}")
            elif entry.is_dir():
                # Recursively hash subdirectory
                parts.append(f"d:{entry.name}:{hash_directory(Path(entry.path))}")
            elif entry.is_file():
                # Hash file content
                logger.info(f"Start hashing: {entry.name}")
                file_hash = (
                    blake3(max_threads=blake3.AUTO).update_mmap(entry_path).hexdigest()
                )
                parts.append(f"f:{entry.name}:{file_hash}")
        except PermissionError as exc:
            logger.error(f"Permission denied accessing {entry_path}: {exc}")
            raise
        except OSError as exc:
            logger.error(f"Error accessing {entry_path}: {exc}")
            raise

    parts.sort()
    return blake3("\0".join(parts).encode()).hexdigest()


def validate_path(path: str):
    base_path = Path(path)
    if not base_path.exists():
        print(f"❌ Error: {path} does not exist")
        sys.exit(1)

    if not base_path.is_dir():
        print(f"❌ Error: {base_path} should be a directory")
        sys.exit(1)


class ArgumentParserWithHelp(argparse.ArgumentParser):
    def error(self, message):
        """Override to show help message on error"""
        self.print_help()
        self.exit(2, f"\n{self.prog}: ❌ Error: {message}\n")


def main():
    parser = ArgumentParserWithHelp(
        prog="oic", description="Generate checksum to verify with OICM platform"
    )
    parser.add_argument(
        "path", help="Directory to scan when generating the checksum (recursive)"
    )
    parser.add_argument(
        "-c",
        "--checksum",
        help="The reference checksum to compare with the computed value",
    )
    args = parser.parse_args()
    validate_path(args.path)
    checksum = hash_directory(args.path)
    print("Checksum:", checksum)
    if args.checksum and args.checksum == checksum:
        print("\n✅ Checksum verified")


if __name__ == "__main__":
    main()
