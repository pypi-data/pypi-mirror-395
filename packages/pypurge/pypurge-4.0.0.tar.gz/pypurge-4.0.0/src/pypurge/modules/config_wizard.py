from __future__ import annotations
import json
import logging
from pathlib import Path
from .ui import print_info, print_success, get_colors

logger = logging.getLogger(__name__)

def run_init_wizard() -> int:
    """
    Runs the configuration wizard to generate a .pypurge.json file.
    """
    colors = get_colors(True) # Force colors for interactive mode
    print_info("Welcome to the pypurge configuration wizard!", colors)
    print("This will guide you through creating a .pypurge.json file.\n")

    config = {
        "standard_rules": True,
        "exclude_dirs": [],
        "exclude_patterns": []
    }

    # 1. Standard rules
    try:
        ans = input("Do you want to enable standard Python cleanup rules? (y/n) [y]: ").strip().lower()
    except EOFError:
        ans = "y"

    if ans == "n":
        config["standard_rules"] = False
        print("Standard rules disabled.")
    else:
        print("Standard rules enabled.")

    # 2. Custom directory exclusions
    try:
        ans = input("\nDo you want to add custom directory exclusions?\n(comma-separated list, e.g. my_dir,other_dir, or enter to skip): ").strip()
    except EOFError:
        ans = ""

    if ans:
        dirs = [d.strip() for d in ans.split(",") if d.strip()]
        config["exclude_dirs"] = dirs
        print(f"Added {len(dirs)} directory exclusions.")

    # 3. Custom file exclusions
    try:
        ans = input("\nDo you want to add custom file exclusions?\n(comma-separated list, e.g. *.txt,secret.key, or enter to skip): ").strip()
    except EOFError:
        ans = ""

    if ans:
        patterns = [p.strip() for p in ans.split(",") if p.strip()]
        config["exclude_patterns"] = patterns
        print(f"Added {len(patterns)} file exclusions.")

    # Write file
    target_path = Path(".pypurge.json")
    if target_path.exists():
        try:
            overwrite = input(f"\n{target_path} already exists. Overwrite? (y/n) [n]: ").strip().lower()
        except EOFError:
            overwrite = "n"
        if overwrite != "y":
            print_info("Aborted.", colors)
            return 0

    try:
        with open(target_path, "w") as f:
            json.dump(config, f, indent=2)
        print_success(f"\nSuccessfully created {target_path.resolve()}", colors)
        logger.info("Created config file %s", target_path)
    except Exception as e:
        logger.error("Failed to write config file: %s", e)
        print(f"Error: {e}")
        return 1

    return 0
