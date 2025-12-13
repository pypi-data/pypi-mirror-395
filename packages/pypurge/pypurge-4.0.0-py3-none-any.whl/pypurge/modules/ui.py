# src/pypurge/modules/ui.py

from pathlib import Path
from typing import List, Tuple

from .utils import format_bytes, get_size


class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    GRAY = "\033[0;90m"
    NC = "\033[0m"


class NullColors:
    RED = GREEN = YELLOW = BLUE = CYAN = GRAY = NC = ""


def get_colors(use_color: bool):
    return Colors() if use_color else NullColors()


def print_info(msg: str, colors):
    print(f"{colors.BLUE}ℹ️  {msg}{colors.NC}")


def print_success(msg: str, colors):
    print(f"{colors.GREEN}✅ {msg}{colors.NC}")


def print_warning(msg: str, colors):
    print(f"{colors.YELLOW}⚠️  {msg}{colors.NC}")


def print_error(msg: str, colors):
    print(f"{colors.RED}❌ {msg}{colors.NC}")


def summarize_groups(targets: dict) -> List[Tuple[str, int, int]]:
    """Return list of tuples (group_name, item_count, total_bytes) sorted by total_bytes desc."""
    res = []
    for g, items in targets.items():
        cnt = len(items)
        size = sum(get_size(p) for p in items)
        res.append((g, cnt, size))
    res.sort(key=lambda x: (x[2], x[1]), reverse=True)
    return res


def print_rich_preview(root_path: Path, targets: dict, sizes: dict, colors):
    # summary table
    summary = summarize_groups(targets)
    print()
    print(
        f"{colors.CYAN}=== Preview: grouped cleanup summary for {root_path}{colors.NC}"
    )
    print(f"{colors.GRAY}Groups shown sorted by total size (largest first){colors.NC}")
    print()
    # header
    print(
        f" {colors.BLUE}Group{' ' * 30} Items   Size{' ' * 10}Paths (truncated){colors.NC}"
    )
    print(f" {colors.BLUE}{'-' * 70}{colors.NC}")
    for g, cnt, total in summary:
        size_s = format_bytes(total)
        name = g
        print(f" {colors.YELLOW}{name:35}{colors.NC} {cnt:5d}   {size_s:12} ")
    print()
    # detailed listing for each group (top 30 entries per group to avoid flood)
    for g, cnt, total in summary:
        print(
            f"{colors.BLUE}\n📁 {g} — {cnt} item(s), {format_bytes(total)}{colors.NC}"
        )
        group_items = sorted(targets.get(g, []), key=lambda p: (p.is_dir(), str(p)))
        preview_items = group_items[:30]
        for p in preview_items:
            try:
                rel = p.relative_to(root_path)
            except Exception:
                rel = p
            suffix = (
                "/"
                if p.is_dir() and not p.is_symlink()
                else " (symlink)"
                if p.is_symlink()
                else ""
            )
            print(f"   {rel}{suffix} — {format_bytes(sizes.get(p, 0))}")
        if cnt > len(preview_items):
            print(f"   ... and {cnt - len(preview_items)} more items in this group ...")
    print()
