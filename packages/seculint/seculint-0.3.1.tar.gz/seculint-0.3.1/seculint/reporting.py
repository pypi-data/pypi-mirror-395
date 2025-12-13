import json
import sys
from pathlib import Path
from typing import List

from .models import Finding

RESET = "\033[0m"
BOLD = "\033[1m"

FG_RED = "\033[31m"
FG_YELLOW = "\033[33m"
FG_GREEN = "\033[32m"
FG_MAGENTA = "\033[35m"
FG_WHITE = "\033[37m"

SEVERITY_COLOR = {
    "HIGH": FG_RED,
    "MEDIUM": FG_YELLOW,
    "LOW": FG_GREEN,
}

USE_COLOR = True  # can be toggled later via CLI if you add --no-color


def colored(text: str, color: str) -> str:
    if not USE_COLOR:
        return text
    return f"{color}{text}{RESET}"


def print_findings_console(findings: List[Finding], use_ai: bool = False) -> None:
    if not findings:
        print(colored("\n✅ SecuLint: No potential secrets or privacy leaks found.", FG_GREEN))
        return

    print(colored("\n⚠️  SecuLint: Potential secrets / privacy leaks found:\n", FG_RED))

    for f in findings:
        eff_sev = f.effective_severity()
        sev_color = SEVERITY_COLOR.get(eff_sev, FG_WHITE)
        sev_text = colored(eff_sev, sev_color)

        print(f"{BOLD}File      :{RESET} {f.file_path}")
        print(f"{BOLD}Line      :{RESET} {f.line_no}")
        print(f"{BOLD}Pattern   :{RESET} {f.pattern_name} (severity: {sev_text})")
        print(f"{BOLD}Desc      :{RESET} {f.description}")
        print(f"{BOLD}Snippet   :{RESET} {colored(f.line_preview.strip(), FG_MAGENTA)}")

        if use_ai:
            print(f"  AI Confirmed : {f.ai_confirmed}")
            print(f"  AI Severity  : {f.ai_severity}")
            print(f"  AI Type      : {f.ai_type}")
            print(f"  Reason       : {f.ai_reason}")


        print(colored("-" * 80, FG_WHITE))


def save_findings_json(findings: List[Finding], json_path: Path) -> None:
    data = [f.to_dict() for f in findings]
    try:
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] JSON report saved to {json_path}")
    except OSError as e:
        print(f"[ERROR] Could not save JSON report to {json_path}: {e}", file=sys.stderr)


def save_findings_html(findings: List[Finding], html_path: Path) -> None:
    total = len(findings)
    high = sum(1 for f in findings if f.effective_severity() == "HIGH")
    medium = sum(1 for f in findings if f.effective_severity() == "MEDIUM")
    low = sum(1 for f in findings if f.effective_severity() == "LOW")

    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    if findings:
        rows = []
        for f in findings:
            sev = f.effective_severity()
            sev_class = sev.lower()
            ai_badge = ""
            if f.ai_confirmed is not None:
                ai_badge = f'<div class="ai-pill">AI: {"✔" if f.ai_confirmed else "✖"} {esc(f.ai_severity or "")}</div>'
            ai_reason = esc(f.ai_reason) if f.ai_reason else ""
            rows.append(
                f"""
            <tr class="row-{sev_class}">
                <td class="col-file">{esc(f.file_path)}</td>
                <td class="col-line">{f.line_no}</td>
                <td class="col-pattern">{esc(f.pattern_name)}</td>
                <td class="col-severity">
                    <span class="badge badge-{sev_class}">{esc(sev)}</span>
                    {ai_badge}
                </td>
                <td class="col-desc">
                    {esc(f.description)}
                    <div class="ai-reason">{ai_reason}</div>
                </td>
                <td class="col-snippet"><pre>{esc(f.line_preview)}</pre></td>
            </tr>
            """
            )
        rows_html = "\n".join(rows)
    else:
        rows_html = """
        <tr>
            <td colspan="6" class="no-findings">No potential secrets or privacy leaks found.</td>
        </tr>
        """

    # (HTML template exactly as you had, with theme toggle)
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<title>SecuLint Report</title>
<style>
    :root {{
        --bg: #0f172a;
        --bg-alt: #020617;
        --bg-card: #020617;
        --bg-hover: #0b1120;
        --border-subtle: #1f2937;
        --border-soft: #111827;
        --text-main: #e5e7eb;
        --text-muted: #9ca3af;
        --text-softer: #6b7280;
        --accent: #38bdf8;
        --accent-secondary: #f97316;
    }}

    :root[data-theme="light"] {{
        --bg: #f9fafb;
        --bg-alt: #ffffff;
        --bg-card: #ffffff;
        --bg-hover: #e5e7eb;
        --border-subtle: #d1d5db;
        --border-soft: #e5e7eb;
        --text-main: #111827;
        --text-muted: #6b7280;
        --text-softer: #9ca3af;
        --accent: #2563eb;
        --accent-secondary: #f97316;
    }}

    body {{
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: var(--bg);
        color: var(--text-main);
        margin: 0;
        padding: 0;
    }}
    .container {{
        max-width: 1200px;
        margin: 40px auto;
        padding: 24px;
        background: var(--bg-card);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(15,23,42,0.7);
        border: 1px solid var(--border-subtle);
    }}

    .toolbar {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 12px;
    }}
    .theme-toggle {{
        border-radius: 999px;
        border: 1px solid var(--border-subtle);
        background: var(--bg-alt);
        color: var(--text-main);
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .theme-toggle:hover {{
        background: var(--bg-hover);
    }}

    h1 {{
        margin-top: 0;
        font-size: 26px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    h1 .logo {{
        font-weight: 700;
        color: var(--accent);
    }}
    h1 .dot {{
        color: var(--accent-secondary);
    }}
    .summary {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 18px 0 24px 0;
    }}
    .summary-card {{
        background: var(--bg-alt);
        border-radius: 10px;
        padding: 10px 14px;
        border: 1px solid var(--border-subtle);
        min-width: 160px;
    }}
    .summary-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
    }}
    .summary-value {{
        margin-top: 6px;
        font-size: 20px;
        font-weight: 600;
    }}
    .summary-value.total {{ color: var(--accent); }}
    .summary-value.high {{ color: #f97373; }}
    .summary-value.medium {{ color: #facc15; }}
    .summary-value.low {{ color: #4ade80; }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
        font-size: 13px;
        table-layout: fixed;
    }}
    thead tr {{
        background: var(--bg-alt);
    }}
    thead th {{
        text-align: left;
        padding: 10px 8px;
        border-bottom: 1px solid var(--border-subtle);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
    }}
    tbody tr:nth-child(even) {{
        background: var(--bg-card);
    }}
    tbody tr:nth-child(odd) {{
        background: var(--bg-card);
    }}
    tbody tr:hover {{
        background: var(--bg-hover);
    }}
    td {{
        padding: 8px;
        vertical-align: top;
        border-bottom: 1px solid var(--border-soft);
    }}

    .col-file {{
        width: 18%;
        font-family: "JetBrains Mono", Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        white-space: normal;
        overflow-wrap: anywhere;
    }}
    .col-line {{
        width: 4%;
        text-align: center;
        color: var(--text-muted);
    }}
    .col-pattern {{
        width: 10%;
        font-weight: 500;
        white-space: normal;
        overflow-wrap: anywhere;
    }}
    .col-severity {{
        width: 10%;
        text-align: center;
    }}
    .col-desc {{
        width: 18%;
        color: var(--text-muted);
        white-space: normal;
        overflow-wrap: anywhere;
    }}
    .col-snippet {{
        width: 40%;
    }}
    .col-snippet pre {{
        margin: 0;
        padding: 10px 12px;
        background: var(--bg);
        border-radius: 6px;
        font-family: "JetBrains Mono", Menlo, Monaco, Consolas, monospace;
        font-size: 12px;
        color: var(--text-main);
        white-space: pre-wrap;
        word-break: break-word;
        overflow-x: auto;
        border: 1px solid var(--border-soft);
    }}

    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}
    .badge-high {{
        background: rgba(248,113,113,0.08);
        color: #fecaca;
        border: 1px solid rgba(248,113,113,0.4);
    }}
    .badge-medium {{
        background: rgba(250,204,21,0.08);
        color: #fef08a;
        border: 1px solid rgba(250,204,21,0.4);
    }}
    .badge-low {{
        background: rgba(52,211,153,0.08);
        color: #bbf7d0;
        border: 1px solid rgba(52,211,153,0.4);
    }}
    .ai-pill {{
        margin-top: 4px;
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 999px;
        border: 1px solid #4b5563;
        color: #9ca3af;
        display: inline-block;
    }}
    .ai-reason {{
        margin-top: 4px;
        font-size: 11px;
        color: var(--text-softer);
    }}
    .no-findings {{
        text-align: center;
        padding: 32px;
        color: var(--text-muted);
    }}
    .footer {{
        margin-top: 20px;
        font-size: 11px;
        color: var(--text-softer);
        text-align: right;
    }}
    .footer .brand {{
        color: var(--accent);
        font-weight: 600;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="toolbar">
        <button id="theme-toggle" class="theme-toggle">🌙 Dark</button>
    </div>

    <h1><span class="logo">SecuLint</span><span class="dot">•</span> Secrets & Privacy Leak Report</h1>

    <div class="summary">
        <div class="summary-card">
            <div class="summary-label">Total Findings</div>
            <div class="summary-value total">{total}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">High Severity</div>
            <div class="summary-value high">{high}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">Medium Severity</div>
            <div class="summary-value medium">{medium}</div>
        </div>
        <div class="summary-card">
            <div class="summary-label">Low Severity</div>
            <div class="summary-value low">{low}</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>File</th>
                <th>Line</th>
                <th>Pattern</th>
                <th>Severity</th>
                <th>Description</th>
                <th>Snippet</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="footer">
        Generated by <span class="brand">SecuLint</span> — Local Secret & Privacy Leak Scanner (with AI assist)
    </div>
</div>

<script>
(function() {{
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');

    function applyLabel(theme) {{
        if (!btn) return;
        if (theme === 'light') {{
            btn.textContent = '☀️ Light';
        }} else {{
            btn.textContent = '🌙 Dark';
        }}
    }}

    function setTheme(theme) {{
        root.setAttribute('data-theme', theme);
        try {{
            localStorage.setItem('seculint-theme', theme);
        }} catch (e) {{}}
        applyLabel(theme);
    }}

    let stored = null;
    try {{
        stored = localStorage.getItem('seculint-theme');
    }} catch (e) {{}}

    const initial = stored || 'dark';
    setTheme(initial);

    if (btn) {{
        btn.addEventListener('click', function () {{
            const current = root.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            setTheme(next);
        }});
    }}
}})();
</script>
</body>
</html>"""

    try:
        with html_path.open("w", encoding="utf-8") as f:
            f.write(html)
        print(f"[INFO] HTML report saved to {html_path}")
    except OSError as e:
        print(f"[ERROR] Could not save HTML report to {html_path}: {e}", file=sys.stderr)
