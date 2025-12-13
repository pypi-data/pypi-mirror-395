import json
import os
from pathlib import Path
from typing import Dict, List

from .models import Finding

try:
    import openai  # type: ignore
except ImportError:
    openai = None


def get_line_context(file_path: Path, line_no: int, radius: int = 5) -> str:
    try:
        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return ""
    start = max(0, line_no - 1 - radius)
    end = min(len(lines), line_no - 1 + radius)
    return "\n".join(f"{i+1:4}: {lines[i]}" for i in range(start, end))


def call_ai_model(prompt: str, model: str = "gpt-4o-mini") -> str:
    if openai is None:
        raise RuntimeError(
            "openai library is not installed. Install with 'pip install openai' to use --enable-ai."
        )
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment, required for --enable-ai.")
    openai.api_key = api_key

    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a security code reviewer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    return resp["choices"][0]["message"]["content"]


def analyze_finding_with_ai(finding: Finding, file_context: str) -> Dict:
    prompt = f"""
You are a senior application security engineer.

You are reviewing this code context:

{file_context}

A potential finding was detected by a regex-based scanner:

- File: {finding.file_path}
- Line: {finding.line_no}
- Pattern: {finding.pattern_name}
- Snippet: {finding.line_preview}

Questions:
1. Is this actually a secret or sensitive data or truly security-relevant? (true/false)
2. If yes, what type? (e.g., password, token, API key, private key, PII, debug_flag, false_positive, etc.)
3. What severity would you assign? (LOW, MEDIUM, HIGH)
4. Give a short reason (max 2 sentences).

Respond ONLY in strict JSON, with keys:
  "is_secret" (boolean),
  "secret_type" (string),
  "severity" (string: LOW|MEDIUM|HIGH),
  "reason" (string).
"""
    text = call_ai_model(prompt)
    text = text.strip()

    # Handle case where model wraps JSON in ```json ... ```
    json_str = text
    if text.startswith("```"):
        lines = text.splitlines()
        json_lines = [ln for ln in lines if not ln.strip().startswith("```")]
        json_str = "\n".join(json_lines).strip()

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {
            "is_secret": True,
            "secret_type": finding.pattern_name,
            "severity": finding.severity,
            "reason": "AI response was not valid JSON; falling back to regex classification.",
        }
    return data


def ai_refine_findings(findings: List[Finding]) -> List[Finding]:
    refined: List[Finding] = []

    for f in findings:
        try:
            context = get_line_context(Path(f.file_path), f.line_no, radius=6)
            analysis = analyze_finding_with_ai(f, context)

            # Ensure safe defaults even if AI gives garbage or empty JSON
            f.ai_confirmed = bool(analysis.get("is_secret", False))
            f.ai_type = analysis.get("secret_type", f.pattern_name)
            sev = analysis.get("severity", f.severity)
            f.ai_severity = sev.upper() if isinstance(sev, str) else f.severity.upper()
            f.ai_reason = analysis.get("reason", "No AI reason provided.")

            refined.append(f)

        except Exception as e:
            # Fail-safe fallback: never return None values
            f.ai_confirmed = True           # treat as real secret
            f.ai_type = f.pattern_name
            f.ai_severity = f.severity
            f.ai_reason = f"[AI ERROR] {e}"
            refined.append(f)

    # Only drop AI-rejected findings (False)
    return [x for x in refined if x.ai_confirmed is True]
