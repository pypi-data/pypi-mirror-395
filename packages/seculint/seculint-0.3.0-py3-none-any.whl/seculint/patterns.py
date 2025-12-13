import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# Base pattern definitions
PATTERN_DEFINITIONS = [
    # ===== Secrets =====
    {
        "name": "AWS_ACCESS_KEY_ID",
        "regex": re.compile(r"AKIA[0-9A-Z]{16}"),
        "description": "Possible AWS Access Key ID.",
        "severity": "HIGH",
    },
    {
        "name": "GENERIC_PASSWORD_ASSIGNMENT",
        "regex": re.compile(
            r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*[\"']?[^\"'\s]+[\"']?"
        ),
        "description": "Line looks like it contains a password.",
        "severity": "HIGH",
    },
    {
        "name": "GENERIC_TOKEN_ASSIGNMENT",
        "regex": re.compile(
            r"(?i)\b(token|access_token|auth_token|bearer_token|secret)\b\s*[:=]\s*[\"']?[^\"'\s]+[\"']?"
        ),
        "description": "Line looks like it contains a token/secret.",
        "severity": "HIGH",
    },
    {
        "name": "PRIVATE_KEY_MARKER",
        "regex": re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
        "description": "Private key material found.",
        "severity": "HIGH",
    },
    # ===== Privacy / PII =====
    {
        "name": "EMAIL_ADDRESS",
        "regex": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "description": "Email address found (possible PII).",
        "severity": "MEDIUM",
    },
    {
        "name": "PHONE_NUMBER",
        "regex": re.compile(
            r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{3}[-.\s]\d{3}[-.\s]\d{4}|\d{4}[-.\s]\d{7})\b"
        ),
        "description": "Phone number like pattern found (possible PII).",
        "severity": "MEDIUM",
    },
    # ===== Insecure patterns =====
    {
        "name": "DISABLE_TLS_VERIFICATION",
        "regex": re.compile(r"verify\s*=\s*False"),
        "description": "TLS verification disabled (verify=False).",
        "severity": "HIGH",
    },
    {
        "name": "DEBUG_TRUE",
        "regex": re.compile(r"\bDEBUG\s*=\s*True\b"),
        "description": "DEBUG=True committed (may leak sensitive info).",
        "severity": "LOW",
    },
]


def load_pattern_config(path: Path) -> Dict[str, Dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[WARN] Failed to load config {path}: {e}", file=sys.stderr)
        return {}

    patterns_cfg = data.get("patterns", {})
    if not isinstance(patterns_cfg, dict):
        print(
            f"[WARN] Invalid config structure in {path}: missing 'patterns' dict.",
            file=sys.stderr,
        )
        return {}
    return patterns_cfg


def build_active_patterns(pattern_config: Dict[str, Dict]) -> List[Dict]:
    """
    Merge default pattern definitions with overrides from config.
    """
    active: List[Dict] = []
    for p in PATTERN_DEFINITIONS:
        name = p["name"]
        cfg = pattern_config.get(name, {})
        enabled = cfg.get("enabled", True)
        if not enabled:
            continue

        severity = cfg.get("severity", p["severity"]).upper()
        pattern_copy = dict(p)
        pattern_copy["severity"] = severity
        active.append(pattern_copy)

    return active
