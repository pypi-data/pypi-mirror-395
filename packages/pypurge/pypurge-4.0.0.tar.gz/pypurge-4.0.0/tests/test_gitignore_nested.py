
import os
from pathlib import Path
from pypurge.modules.scan import scan_for_targets

def test_nested_gitignore_skip_directory(fs):
    """
    Test that a nested .gitignore file prevents traversal into ignored directories,
    protecting files inside them from being scanned and deleted.
    """
    root = Path("/project")
    fs.create_dir(root)

    # Structure:
    # /project/nested/.gitignore -> ignores "ignored_deep/"
    # /project/nested/ignored_deep/data.tmp -> Should NOT be touched (because dir is ignored)
    # /project/nested/visible_deep/data.tmp -> Should be touched (normal dir)

    nested = root / "nested"
    fs.create_dir(nested)

    # Create nested .gitignore
    fs.create_file(nested / ".gitignore", contents="ignored_deep/\n")

    # Create ignored directory and file inside
    ignored_deep = nested / "ignored_deep"
    fs.create_dir(ignored_deep)
    fs.create_file(ignored_deep / "data.tmp")

    # Create visible directory and file inside
    visible_deep = nested / "visible_deep"
    fs.create_dir(visible_deep)
    fs.create_file(visible_deep / "data.tmp")

    # Targets
    file_groups = {"Temps": ["*.tmp"]}

    targets = scan_for_targets(
        root_path=root,
        dir_groups={},
        file_groups=file_groups,
        exclude_dirs=set(),
        exclude_patterns=[],
        older_than_sec=0,
        age_type="mtime",
        delete_symlinks=False,
        use_gitignore=True
    )

    all_targets = [p for sublist in targets.values() for p in sublist]

    # Verify visible file is targeted
    assert visible_deep / "data.tmp" in all_targets

    # Verify ignored file is NOT targeted (this should fail currently)
    assert ignored_deep / "data.tmp" not in all_targets
