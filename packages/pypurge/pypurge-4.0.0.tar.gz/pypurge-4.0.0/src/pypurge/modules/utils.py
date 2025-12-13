# src/pypurge/modules/utils.py

import hashlib
import time
from pathlib import Path


def format_bytes(bytes_size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(bytes_size)
    unit = 0
    while size >= 1024 and unit < len(units) - 1:
        size /= 1024
        unit += 1
    return f"{size:.2f}{units[unit]}" if unit > 0 else f"{int(size)}{units[unit]}"


def get_size(path: Path) -> int:
    total = 0
    try:
        if path.is_symlink():
            return int(path.lstat().st_size or 0)
        if path.is_file():
            return int(path.stat().st_size or 0)
        for sub in path.rglob("*"):
            try:
                if sub.is_file():
                    total += int(sub.stat().st_size or 0)
                elif sub.is_symlink():
                    total += int(sub.lstat().st_size or 0)
            except Exception:
                continue
    except Exception:
        return 0
    return total


def is_old_enough(path: Path, older_than_sec: float, age_type: str) -> bool:
    try:
        st = path.stat()
        if age_type == "mtime":
            t = st.st_mtime
        elif age_type == "atime":
            t = st.st_atime
        elif age_type == "ctime":
            t = st.st_ctime
        else:
            t = st.st_mtime
        return t < time.time() - older_than_sec
    except Exception:
        return False


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
