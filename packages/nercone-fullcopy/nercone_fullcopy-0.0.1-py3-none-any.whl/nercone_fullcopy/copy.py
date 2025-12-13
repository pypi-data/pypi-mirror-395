from __future__ import annotations

import errno
import fcntl
import hashlib
import os
import stat
import struct
from typing import Optional

from nercone_modern.logging import ModernLogging
from nercone_modern.progressbar import ModernProgressBar

BLKGETSIZE64 = 0x80081272


def human_size(value: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{value} B"


def parse_size(text: str) -> int:
    suffixes = {
        "k": 1024,
        "kb": 1024,
        "m": 1024 ** 2,
        "mb": 1024 ** 2,
        "g": 1024 ** 3,
        "gb": 1024 ** 3,
        "t": 1024 ** 4,
        "tb": 1024 ** 4,
    }
    normalized = text.strip().lower()
    for suffix, factor in suffixes.items():
        if normalized.endswith(suffix):
            number = normalized[: -len(suffix)].strip()
            return int(float(number) * factor)
    return int(normalized)


def detect_media_size(path: str, logger: ModernLogging) -> Optional[int]:
    try:
        st = os.stat(path)
    except OSError as exc:
        logger.log(f"Failed to stat '{path}': {exc}", level_text="ERROR", level_color="red")
        return None

    if stat.S_ISREG(st.st_mode) and st.st_size > 0:
        return st.st_size

    if stat.S_ISBLK(st.st_mode) or stat.S_ISCHR(st.st_mode):
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        except OSError as exc:
            logger.log(
                f"Cannot open '{path}' to discover size: {exc}",
                level_text="ERROR",
                level_color="red",
            )
            return None
        try:
            buf = fcntl.ioctl(fd, BLKGETSIZE64, b"\0" * 8)
            size = struct.unpack("Q", buf)[0]
            if size > 0:
                return size
        except OSError as exc:
            logger.log(
                f"Kernel refused BLKGETSIZE64 for '{path}': {exc}",
                level_text="WARN",
                level_color="yellow",
            )
        finally:
            os.close(fd)
    return None


def _copy_extended_attributes(src: str, dest: str, logger: ModernLogging) -> None:
    if not hasattr(os, "listxattr") or not hasattr(os, "setxattr"):
        return
    try:
        xattrs = os.listxattr(src)
    except OSError:
        return
    for name in xattrs:
        try:
            value = os.getxattr(src, name)
            os.setxattr(dest, name, value)
        except OSError as exc:
            logger.log(
                f"Failed to copy xattr {name!r}: {exc}", level_text="WARN", level_color="yellow"
            )


def _copy_permissions(src_stat: os.stat_result, dest: str, logger: ModernLogging) -> None:
    try:
        os.chmod(dest, stat.S_IMODE(src_stat.st_mode))
    except OSError as exc:
        logger.log(f"Could not apply permissions: {exc}", level_text="WARN", level_color="yellow")
    try:
        if hasattr(os, "chown"):
            os.chown(dest, src_stat.st_uid, src_stat.st_gid)
    except OSError as exc:
        if exc.errno != errno.EPERM:
            logger.log(f"Could not apply ownership: {exc}", level_text="WARN", level_color="yellow")
    try:
        os.utime(dest, ns=(src_stat.st_atime_ns, src_stat.st_mtime_ns))
    except OSError as exc:
        logger.log(f"Could not apply timestamps: {exc}", level_text="WARN", level_color="yellow")


def _open_dest(path: str, force: bool) -> int:
    flags = os.O_WRONLY | os.O_CREAT
    if force:
        flags |= os.O_TRUNC
    try:
        return os.open(path, flags)
    except FileExistsError:
        raise


def copy_raw(
    source: str,
    destination: str,
    logger: ModernLogging,
    block_size: int = 4 * 1024 * 1024,
    declared_size: Optional[int] = None,
    force: bool = False,
    flush: bool = False,
) -> int:
    size = declared_size if declared_size and declared_size > 0 else detect_media_size(source, logger)
    spinner = size is None
    progress = ModernProgressBar(total=size or 1, process_name="copy", spinner_mode=spinner)
    if spinner:
        progress.spin_start()
    progress.setMessage("Copying data blocks")

    try:
        src_fd = os.open(source, os.O_RDONLY)
    except OSError as exc:
        raise RuntimeError(f"Unable to open source: {exc}") from exc

    try:
        if os.path.exists(destination):
            st = os.stat(destination)
            if stat.S_ISREG(st.st_mode) and not force:
                raise RuntimeError("Destination exists. Use --force to overwrite.")
        dest_fd = _open_dest(destination, force=force)
    except OSError as exc:
        os.close(src_fd)
        raise RuntimeError(f"Unable to open destination: {exc}") from exc

    copied = 0
    try:
        while True:
            chunk = os.read(src_fd, block_size)
            if not chunk:
                break
            view = memoryview(chunk)
            total_written = 0
            while total_written < len(view):
                written = os.write(dest_fd, view[total_written:])
                total_written += written
            copied += len(chunk)
            if not spinner:
                progress.update(len(chunk))
                progress.setMessage(
                    f"Copying {human_size(copied)} / {human_size(size or copied)}"
                )
            else:
                progress.update()
        if flush:
            os.fsync(dest_fd)
    finally:
        os.close(src_fd)
        os.close(dest_fd)
        progress.finish()

    try:
        src_stat = os.stat(source)
        if stat.S_ISREG(src_stat.st_mode):
            _copy_permissions(src_stat, destination, logger)
            _copy_extended_attributes(source, destination, logger)
    except OSError as exc:
        logger.log(f"Metadata preservation best-effort failed: {exc}", level_text="WARN", level_color="yellow")

    return copied


def _hash_stream(path: str, algo: str, block_size: int, size: Optional[int], logger: ModernLogging) -> str:
    hasher = hashlib.new(algo)
    spinner = size is None
    progress = ModernProgressBar(total=size or 1, process_name=f"hash-{os.path.basename(path) or 'target'}", spinner_mode=spinner)
    if spinner:
        progress.spin_start()
    progress.setMessage("Calculating integrity")
    processed = 0
    try:
        with open(path, "rb", buffering=0) as fh:
            while True:
                chunk = fh.read(block_size)
                if not chunk:
                    break
                hasher.update(chunk)
                processed += len(chunk)
                if spinner:
                    progress.update()
                else:
                    progress.update(len(chunk))
                    progress.setMessage(
                        f"Hashed {human_size(processed)} / {human_size(size or processed)}"
                    )
    finally:
        progress.finish()
    digest = hasher.hexdigest()
    logger.log(
        f"Hash for {path}: {digest}",
        level_text="INFO",
        level_color="green",
    )
    return digest


def verify_integrity(
    source: str,
    destination: str,
    logger: ModernLogging,
    block_size: int,
    algo: str,
    declared_size: Optional[int] = None,
) -> bool:
    size = declared_size if declared_size and declared_size > 0 else detect_media_size(source, logger)
    source_hash = _hash_stream(source, algo, block_size, size, logger)
    dest_hash = _hash_stream(destination, algo, block_size, size, logger)
    if source_hash == dest_hash:
        logger.log("Integrity check passed", level_text="INFO", level_color="green")
        return True
    logger.log(
        "Integrity check FAILED: source and destination differ", level_text="ERROR", level_color="red"
    )
    return False
