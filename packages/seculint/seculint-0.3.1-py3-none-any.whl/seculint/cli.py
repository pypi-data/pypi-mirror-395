import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from . import __version__
from .git_utils import get_changed_files
from .ai_integration import ai_refine_findings, openai  # type: ignore
from .ignore import load_ignore_patterns
from .models import Finding
from .patterns import build_active_patterns, load_pattern_config
from .reporting import print_findings_console, save_findings_html, save_findings_json
from .scanner import walk_and_scan, should_scan_file




from .scanner import walk_and_scan, should_scan_file, scan_file
from .ignore import load_ignore_patterns

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="seculint",
        description=(
            "SecuLint — Lightweight Secret & Privacy Leak Scanner "
            "for local repositories with optional AI-assisted analysis."
        ),
        epilog=(
            "Examples:\n"
            "  seculint --path .\n"
            "  seculint --path ./src --include-ext .py .env\n"
            "  seculint --path . --enable-ai --html-report results.html\n"
            "  seculint --path . --changed-only\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--path",
        required=True,
        help=(
            "Root directory or single file to scan.\n"
            "Example: --path ./src  or  --path config/settings.py"
        ),
    )

    parser.add_argument(
        "--max-size-mb",
        type=int,
        default=5,
        help=(
            "Maximum file size (in MB) to scan.\n"
            "Files larger than this limit will be skipped. Default: 5 MB."
        ),
    )

    parser.add_argument(
        "--include-ext",
        nargs="*",
        default=None,
        help=(
            "Optional list of file extensions to include.\n"
            "Example: --include-ext .py .env .json"
        ),
    )

    parser.add_argument(
        "--exclude-ext",
        nargs="*",
        default=None,
        help=(
            "Optional list of file extensions to exclude.\n"
            "Example: --exclude-ext .log .md"
        ),
    )

    parser.add_argument(
        "--json-report",
        default=None,
        help=(
            "Path to save findings as JSON file.\n"
            "Example: --json-report reports/findings.json"
        ),
    )

    parser.add_argument(
        "--html-report",
        default=None,
        help=(
            "Path to save findings as a styled HTML report.\n"
            "Example: --html-report reports/findings.html"
        ),
    )

    parser.add_argument(
        "--config",
        default=None,
        help=(
            "Optional JSON config file to customize pattern behavior.\n"
            "Supports enabling/disabling patterns and overriding severities.\n"
            "Example structure:\n"
            '{\n'
            '  "patterns": {\n'
            '    "AWS_SECRET_KEY": {"enabled": true, "severity": "HIGH"}\n'
            '  }\n'
            '}'
        ),
    )

    parser.add_argument(
        "--enable-ai",
        action="store_true",
        help=(
            "Enable AI refinement and explanation of detected findings.\n"
            "Requires `openai` library and a valid `OPENAI_API_KEY` environment variable."
        ),
    )

    parser.add_argument(
        "--changed-only",
        action="store_true",
        help=(
            "Scan only changed (staged/unstaged) files in the current Git repository.\n"
            "Useful for pre-commit or CI/CD hooks."
        ),
    )

    parser.add_argument(
        "--debug-ignore",
        action="store_true",
        help=(
            "Print debug messages for ignored files and folders "
            "(based on .seculintignore rules)."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"seculint {__version__}",
        help="Display the installed SecuLint version and exit.",
    )

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    root = Path(args.path)
    print(f"[DEBUG] Root path: {root.resolve()}")

    if not root.exists():
        print(f"[ERROR] Path does not exist: {root}", file=sys.stderr)
        return 1

    # AI pre-flight validation
    if args.enable_ai:
        if openai is None:
            print(
                "[ERROR] --enable-ai was used, but the OpenAI library is not installed.",
                file=sys.stderr,
            )
            print("        Install it with: pip install openai")
            return 3

        if not os.getenv("OPENAI_API_KEY"):
            print(
                "[ERROR] --enable-ai was used, but no OPENAI_API_KEY environment variable is set.",
                file=sys.stderr,
            )
            print("        Set it using:")
            print("        export OPENAI_API_KEY='your_key_here'   (Mac/Linux)")
            print("        setx OPENAI_API_KEY 'your_key_here'      (Windows)")
            return 3

    # Build pattern config (if any)
    pattern_config: Dict[str, Dict] = {}
    if args.config:
        cfg_path = Path(args.config)
        if not cfg_path.exists():
            print(f"[WARN] Config file does not exist: {cfg_path}", file=sys.stderr)
        else:
            pattern_config = load_pattern_config(cfg_path)

    active_patterns = build_active_patterns(pattern_config)

    include_ext = (
        [e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.include_ext]
        if args.include_ext
        else None
    )
    exclude_ext = (
        [e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.exclude_ext]
        if args.exclude_ext
        else None
    )

    ignore_patterns = load_ignore_patterns(root)
    print(f"Ignore patterns are: {ignore_patterns}")
    # =========================
    # Scan
    # =========================
    findings: List[Finding] = []
    max_size_bytes = args.max_size_mb * 1024 * 1024
    print(ignore_patterns)
    if args.changed_only:
        # Require git repo for changed-only mode
        if not (root / ".git").exists():
            print(
                "[ERROR] --changed-only was used, but this folder is not a Git repository.",
                file=sys.stderr,
            )
            print("        Run without --changed-only or initialize git (git init).")
            return 2

        print("[INFO] Scanning only changed (staged/unstaged) files in git...")
        changed_files = get_changed_files(root)

        if not changed_files:
            print("[INFO] No modified or staged files detected — nothing to scan.")
        else:
            for file in changed_files:
                if should_scan_file(
                    file,
                    max_size_bytes,
                    include_ext,
                    exclude_ext,
                    ignore_patterns,
                ):
                    findings.extend(scan_file(file, active_patterns))  # type: ignore[name-defined]
    else:
        findings = walk_and_scan(
            root=root,
            max_size_mb=args.max_size_mb,
            include_ext=include_ext,
            exclude_ext=exclude_ext,
            ignore_patterns=ignore_patterns,
            active_patterns=active_patterns,
            debug_ignore=args.debug_ignore,  
        )

    # =========================
    # Optional AI refinement
    # =========================

    use_ai = bool(args.enable_ai)
    if use_ai and findings:
        try:
            findings = ai_refine_findings(findings)
            print(f"[INFO] AI refinement complete. {len(findings)} findings confirmed by AI.")
        except Exception as e:
            print(f"[ERROR] AI refinement failed: {e}")
            # fail-safe fallback: do NOT break scanning
    # =========================
    # Output
    # =========================

    print_findings_console(findings, use_ai=use_ai)

    if args.json_report:
        save_findings_json(findings, Path(args.json_report))

    if args.html_report:
        save_findings_html(findings, Path(args.html_report))

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
