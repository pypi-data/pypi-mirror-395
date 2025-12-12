# 🇪🇺 AI Act Compliance Scanner (Open Core)

> **The Open Source Standard for EU AI Act Compliance.**
> Don't pay €10k/year for a black box. Check your compliance in 5 seconds.

[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Compliance-Automated-green)]()

## ⚡ The Pain
The **EU AI Act** is here. If your software uses ML libraries (e.g., `torch`, `sklearn`, `face_recognition`), you are likely regulated.
*   **Fines:** Up to 7% of global turnover.
*   **Lawyers:** €500/hour.
*   **Manual Work:** Weeks of spreadsheet hell.

## 🛡️ The Solution
`ai-act-check` is the open-source standard. It scans your code, identifies regulated libraries, and tells you if you are "High Risk."

## 🚀 Quick Start

### 1. Install
```bash
pip install ai-act-check
```

### 2. Scan Your Repo
```bash
ai-act-check scan ./my-project
```
*Output: Immediate detection of High Risk libraries (Biometrics, Critical Infra, Employment).*

### 3. Draft Documentation (Teaser)
```bash
export OPENROUTER_API_KEY="sk-..."
ai-act-check draft scan_results.json
```
*Generates a basic Annex IV draft.*

## 👑 Go Sovereign (Pro)
Need the **Official PDF**, Audit Trails, and Team Management?
The Open Source tool is great for developers, but **Sovereign Cloud** is for companies.

| Feature | Open Source | Sovereign Cloud |
| :--- | :---: | :---: |
| **Static Scan** | ✅ | ✅ |
| **Basic Draft** | ✅ | ✅ |
| **Official Annex IV PDF** | ❌ | ✅ |
| **Context-Aware Wizard** | ❌ | ✅ |
| **Audit Trail** | ❌ | ✅ |
| **Team Management** | ❌ | ✅ |

[**Get the Cure -> Sovereign Cloud**](https://sovereign-code.eu)

## ⚠️ License
This project is licensed under the **AGPL v3**.
If you use this code in a SaaS, you must open-source your SaaS.
For closed-source usage, contact us for a Commercial License.