import subprocess
import sys
from pathlib import Path
from typing import List


def get_changed_files(repo_root: Path) -> List[Path]:
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        print(
            "[WARN] --changed-only used, but this is not a git repo or git is unavailable.",
            file=sys.stderr,
        )
        return []

    files: List[Path] = []
    for line in output.splitlines():
        if not line.strip():
            continue

        status = line[:2].strip()
        file_path = line[3:].strip()

        if status or file_path:
            p = repo_root / file_path
            if p.exists():
                files.append(p)

    return files
