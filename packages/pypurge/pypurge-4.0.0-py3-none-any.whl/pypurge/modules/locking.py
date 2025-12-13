# src/pypurge/modules/locking.py

import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

DEFAULT_LOCK_TTL = 24 * 3600  # 24 hours stale lock threshold

logger = logging.getLogger(__name__)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        if hasattr(os, "kill"):
            os.kill(pid, 0)
            return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        try:
            if sys.platform.startswith("win"):
                import psutil  # type: ignore

                return psutil.pid_exists(pid)
        except Exception:
            return True
    return True


def acquire_lock(
    lock_path: Path, stale_seconds: int = DEFAULT_LOCK_TTL
) -> Optional[int]:
    """Create exclusive lockfile. If existing lock appears stale (PID gone and older than TTL), reap it."""
    try:
        if lock_path.exists():
            try:
                txt = lock_path.read_text()
                pid = None
                started = None
                for line in txt.splitlines():
                    if line.startswith("pid:"):
                        try:
                            pid = int(line.split(":", 1)[1])
                        except Exception:
                            pid = None
                    if line.startswith("started:"):
                        try:
                            started = float(line.split(":", 1)[1])
                        except Exception:
                            started = None
                if pid and _pid_alive(pid):
                    return None
                if started is not None and (time.time() - started) < stale_seconds:
                    return None
                try:
                    lock_path.unlink()
                    logger.warning("Removed stale lockfile %s", lock_path)
                except Exception:
                    logger.debug("Could not remove stale lockfile %s", lock_path)
            except Exception:
                return None
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"pid:{os.getpid()}\nstarted:{time.time()}\n".encode("utf-8"))
        return fd
    except FileExistsError:
        return None
    except Exception as e:
        logger.debug("acquire_lock exception: %s", e)
        return None


def release_lock(fd: Optional[int], lock_path: Path) -> None:
    try:
        if fd is not None:
            try:
                os.close(fd)
            except Exception:
                pass
        try:
            lock_path.unlink(missing_ok=True)
        except Exception:
            pass
    except Exception:
        pass
