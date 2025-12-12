# 🇪🇺 AI Act Compliance Scanner (Sovereign Code)

> **Don't let a €35M fine stop you from shipping.**
> The open-source CLI that maps your code to the EU AI Act (Annex IV) in seconds.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Compliance-Automated-green)]()
[![Sovereign Code CI](https://github.com/svel26/ai-act-check/actions/workflows/ci.yml/badge.svg)](https://github.com/svel26/ai-act-check/actions/workflows/ci.yml)

## ⚡ The Problem
The **EU AI Act** is here. If your software uses ML libraries (e.g., `torch`, `sklearn`, `tensorflow.js`, `gorgonia`), you might be classified as **"High Risk"** under Article 6.
* **Lawyers cost:** €500/hour.
* **Ignorance costs:** Up to 7% of global turnover.
* **Manual compliance:** Boring, error-prone, and slow.

## 🛡️ The Solution
`ai-act-check` is a "Compliance-as-Code" tool. It parses your repository's manifests and code, identifies regulated libraries, and uses an LLM Agent to draft your **Annex IV Technical Documentation**.

## 🚀 Quick Start

### 1. Install
```bash
pip install ai-act-check
```

### 2. The Smoke Test (No API Key needed)

Scan your repo for "High Risk" dependencies locally. It works for Python, Node.js, Go, Rust, Java, Ruby, and PHP.

```bash
ai-act-check scan ./my-project
```

*Output: JSON file with detected libraries and risk triggers.*

### 3. Manual Mode (Interactive)

If your language isn't supported yet, or you want to check specific libraries:

```bash
ai-act-check manual
```

Or via CLI flags:
```bash
ai-act-check scan --libs "tensorflow, face_recognition"
```

### 4. Generate the Legal Draft (Requires API Key)

Turn your code scan into a formal legal draft.

```bash
export OPENROUTER_API_KEY="sk-..."
ai-act-check draft scan_results.json
```

*Output: `ANNEX_IV_DRAFT.txt` written in formal legal prose.*

## 🌍 Supported Languages
We automatically scan the following manifest files for high-risk AI/ML libraries:

*   **Python**: `requirements.txt`, `Pipfile`, `pyproject.toml` (plus AST analysis)
*   **Node.js**: `package.json`
*   **Go**: `go.mod`
*   **Rust**: `Cargo.toml`
*   **Java**: `pom.xml`, `build.gradle`
*   **Ruby**: `Gemfile`
*   **PHP**: `composer.json`

## 📂 How it Works

1.  **Manifest & Code Analysis:** We parse your dependency files and source code to see *what* libraries are used.
2.  **Risk Mapping:** Deterministic mapping of libraries to Annex III use cases (Biometrics, Critical Infra, Employment).
3.  **Agentic Drafting:** An LLM agent (Compl-AI) acts as a Junior Associate to draft the text, strictly grounded in the scan evidence.

## ⚠️ Disclaimer

This tool is for **technical documentation assistance only**. It is not legal advice. You remain responsible for your compliance.
For full conformity assessments and liability protection, visit [Sovereign Code](https://www.google.com/search?q=https://sovereign-code.com).