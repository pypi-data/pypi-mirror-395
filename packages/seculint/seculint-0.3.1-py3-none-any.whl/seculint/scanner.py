import os
from pathlib import Path
from typing import List, Optional, Dict, Iterable
from .ignore import is_ignored
from .models import Finding


def should_scan_file(
    path: Path,
    max_size_bytes: int,
    include_ext: Optional[List[str]],
    exclude_ext: Optional[List[str]],
) -> bool:
    """Applies size, extension, and binary-type filters."""
    if not path.is_file():
        return False

    try:
        size = path.stat().st_size
    except OSError:
        return False

    if size > max_size_bytes:
        return False

    ext = path.suffix.lower()

    if include_ext is not None and ext not in include_ext:
        return False

    if exclude_ext is not None and ext in exclude_ext:
        return False

    binary_exts = {
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".pdf", ".exe", ".dll", ".zip", ".tar", ".so",
        ".pyc", ".db", ".sqlite", ".woff", ".woff2",
    }
    if ext in binary_exts:
        return False

    return True


def scan_file(path: Path, active_patterns: List[Dict]) -> Iterable[Finding]:
    """Reads a file line by line and yields findings for matching patterns."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return

    for i, line in enumerate(text.splitlines(), start=1):
        for p in active_patterns:
            if p["regex"].search(line):
                yield Finding(
                    file_path=str(path),
                    line_no=i,
                    pattern_name=p["name"],
                    severity=p["severity"],
                    description=p["description"],
                    line_preview=line,
                )


def walk_and_scan(
    root: Path,
    max_size_mb: int,
    include_ext: Optional[List[str]],
    exclude_ext: Optional[List[str]],
    ignore_patterns: List[str],
    active_patterns: List[Dict],
    debug_ignore: bool = False,  # 👈 new flag
) -> List[Finding]:
    """
    Recursively walk the directory tree from `root` and scan matching files.
    Properly respects .seculintignore rules and skips ignored directories.
    Set `debug_ignore=True` to print skipped files/directories.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    findings: List[Finding] = []
    root = root.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""

        # === Filter ignored directories ===
        keep_dirs = []
        for d in dirnames:
            rel_subdir = f"{rel_dir}/{d}" if rel_dir else d
            if is_ignored(rel_subdir, ignore_patterns):
                if debug_ignore:
                    print(f"[DEBUG] Skipping directory (ignored): {rel_subdir}")
            else:
                keep_dirs.append(d)
        dirnames[:] = keep_dirs  # modifies walk traversal

        # === Process files ===
        for fname in filenames:
            rel_file = f"{rel_dir}/{fname}" if rel_dir else fname

            if is_ignored(rel_file, ignore_patterns):
                if debug_ignore:
                    print(f"[DEBUG] Skipping file (ignored): {rel_file}")
                continue

            full_path = Path(dirpath) / fname
            if should_scan_file(full_path, max_size_bytes, include_ext, exclude_ext):
                for finding in scan_file(full_path, active_patterns):
                    findings.append(finding)

    return findings
