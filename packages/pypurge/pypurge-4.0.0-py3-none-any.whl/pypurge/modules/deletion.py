# src/pypurge/modules/deletion.py

import os
import shutil
import stat
from pathlib import Path


def force_rmtree(path: Path):
    def onerror(func, p: str, exc_info):
        try:
            os.chmod(p, stat.S_IWUSR)
        except Exception:
            pass
        try:
            func(p)
        except Exception:
            pass

    shutil.rmtree(path, onerror=onerror)


def force_unlink(path: Path):
    try:
        if not os.access(path, os.W_OK):
            try:
                os.chmod(path, stat.S_IWUSR)
            except Exception:
                pass
        path.unlink(missing_ok=True)
    except Exception:
        pass
