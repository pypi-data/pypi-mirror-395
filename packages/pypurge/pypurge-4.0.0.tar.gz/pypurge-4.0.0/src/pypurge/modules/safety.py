# src/pypurge/modules/safety.py

from pathlib import Path

DANGEROUS_ROOTS = {
    Path("/"),
    Path.home(),
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/etc"),
}


def is_dangerous_root(p: Path) -> bool:
    try:
        p_res = p.resolve()
    except Exception:
        return True
    for d in DANGEROUS_ROOTS:
        try:
            if str(p_res) == str(d.resolve()):
                return True
        except Exception:
            continue
    if len(p_res.parts) <= 2:
        return True
    return False
