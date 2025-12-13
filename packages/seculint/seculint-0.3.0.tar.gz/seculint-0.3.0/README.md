<p align="center">
  <a href="https://pypi.org/project/seculint/">
    <img src="https://img.shields.io/pypi/v/seculint?color=blue&label=PyPI%20Version&style=for-the-badge">
  </a>
  <a href="https://pypi.org/project/seculint/">
    <img src="https://img.shields.io/pypi/dm/seculint?color=blueviolet&style=for-the-badge">
  </a>
  <img src="https://img.shields.io/pypi/l/seculint?style=for-the-badge">
  <img src="https://img.shields.io/pypi/pyversions/seculint?style=for-the-badge">
</p>

<h1 align="center">🔒 SecuLint — Secret & Privacy Leak Scanner</h1>
<p align="center"><strong>Version 0.3.0 — New filters, debugging tools, JSON reporting & pattern configs!</strong></p>

--- 

## 📦 Installation

```bash
pip install seculint
```

Run a quick scan:

```bash
seculint --path .
```

Enable AI mode:

```bash
seculint --path . --enable-ai
```

---

# 📝 What is SecuLint?

SecuLint is a fast, offline-first secret & privacy leak scanner detecting:

- Hard-coded credentials
- API keys & OAuth tokens
- JWTs, bearer tokens
- Database passwords & URIs
- Private keys (RSA/PEM)
- Personal data

Outputs include: terminal, JSON reports, HTML reports, and optional AI verification.

---

# 🚀 Key Features

- Recursive scanning  
- JSON/HTML outputs  
- AI-based verification  
- Custom pattern configs  
- Changed-only scanning  
- Debug ignore mode  
- Extension filtering  
- Fast & offline  

---

# 🛠️ CLI Arguments

Includes:

- --path
- --enable-ai
- --changed-only
- --debug-ignore
- --include-ext
- --exclude-ext
- --max-size
- --config
- --json-report

---

# 🧩 Pattern Config Example

```json
{
  "patterns": {
    "AWS_SECRET_KEY": { "enabled": true, "severity": "HIGH" },
    "PRIVATE_KEY": { "enabled": true, "severity": "CRITICAL" }
  }
}
```

---

# 📊 JSON Report Example

```bash
seculint --path . --json-report reports/findings.json
```

---

# 🧪 Example Full Command

```bash
seculint --path .   --include-ext .py .json   --exclude-ext .log   --changed-only   --debug-ignore   --config config/patterns.json   --json-report reports/findings.json   --enable-ai
```

---

# 🗂️ Recommended .seculintignore

```
venv/
dist/
build/
__pycache__/
*.log
*.cache/
node_modules/
```
---

# 📚 Version History

- v0.3.0 — Added filters, JSON reports, config engine, debug-ignore  
- v0.2.0 — Added AI mode  
- v0.1.0 — Initial release  

---

# License

MIT License.
