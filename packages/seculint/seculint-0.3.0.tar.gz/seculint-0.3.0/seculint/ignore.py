import fnmatch
import os
from pathlib import Path
from typing import List


def load_ignore_patterns(root: Path) -> List[str]:
    """
    Load ignore patterns from `.seculintignore` if present.
    Returns a list of patterns (supports glob-style matching).
    """
    ignore_file = root / ".seculintignore"
    if not ignore_file.exists():
        return []

    patterns: List[str] = []
    with open(ignore_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def is_ignored(path: str | Path, ignore_patterns: List[str]) -> bool:
    """
    Check if a given file or directory should be ignored
    based on loaded .seculintignore patterns.
    """
    if not ignore_patterns:
        return False

    # Normalize for consistent comparison
    rel_path = str(path).replace("\\", "/").rstrip("/")

    for pat in ignore_patterns:
        pat = pat.strip().replace("\\", "/").rstrip("/")
        if not pat:
            continue

        # Exact match or wildcard
        if fnmatch.fnmatch(rel_path, pat):
            return True

        # If the pattern ends with '/', treat it as a directory ignore rule
        if pat.endswith("/") and (rel_path == pat[:-1] or rel_path.startswith(pat)):
            return True

        # Handle patterns like "venv" (no slash)
        if "/" not in pat and (rel_path == pat or rel_path.startswith(f"{pat}/")):
            return True

    return False
