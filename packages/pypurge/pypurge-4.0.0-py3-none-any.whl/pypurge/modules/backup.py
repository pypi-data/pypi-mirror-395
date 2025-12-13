# src/pypurge/modules/backup.py

import json
import logging
import os
import tempfile
import zipfile
from datetime import datetime as _dt, timezone
from pathlib import Path
from typing import List, Optional, Tuple

from .utils import sha256_of_file

logger = logging.getLogger(__name__)


def backup_targets_atomic(
    targets: List[Path], backup_root: Path, root: Path, name: Optional[str] = None
) -> Optional[Tuple[Path, str]]:
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = _dt.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    archive_name = (
        f"{name}_{timestamp}.zip" if name else f"cleanpy_backup_{timestamp}.zip"
    )
    final_path = backup_root / archive_name
    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix=f".{archive_name}.", dir=str(backup_root)
    )
    os.close(tmp_fd)
    tmp_path = Path(tmp_path)
    symlink_manifest = []
    try:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in targets:
                try:
                    rel = p.relative_to(root)
                except Exception:
                    rel = Path(p.name)
                if p.is_symlink():
                    try:
                        target = os.readlink(p)
                    except Exception:
                        target = None
                    symlink_manifest.append({"path": str(rel), "target": target})
                    continue
                if p.is_file():
                    try:
                        zf.write(p, arcname=rel)
                    except Exception:
                        logger.warning("Failed to write %s to archive", p)
                elif p.is_dir():
                    for sub in p.rglob("*"):
                        if sub.is_file():
                            try:
                                arc = sub.relative_to(root)
                            except Exception:
                                arc = Path(sub.name)
                            try:
                                zf.write(sub, arcname=arc)
                            except Exception:
                                logger.debug("Skipping file in backup: %s", sub)
            if symlink_manifest:
                zf.writestr(
                    "cleanpy_symlink_manifest.json",
                    json.dumps({"symlinks": symlink_manifest}, indent=2),
                )
        sha = sha256_of_file(tmp_path)
        os.replace(tmp_path, final_path)
        shafile = final_path.with_suffix(final_path.suffix + ".sha256")
        tmp_sha = str(shafile) + ".tmp"
        with open(tmp_sha, "w", encoding="utf-8") as f:
            f.write(sha + "  " + final_path.name + "\n")
        os.replace(tmp_sha, shafile)
        return final_path, sha
    except Exception as e:
        logger.error("Backup failed: %s", e)
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        return None
