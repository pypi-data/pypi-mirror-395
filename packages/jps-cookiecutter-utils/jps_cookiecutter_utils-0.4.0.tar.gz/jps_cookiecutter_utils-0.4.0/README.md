# jps-cookiecutter-utils

![Build](https://github.com/jai-python3/jps-cookiecutter-utils/actions/workflows/test.yml/badge.svg)
![Publish to PyPI](https://github.com/jai-python3/jps-cookiecutter-utils/actions/workflows/publish-to-pypi.yml/badge.svg)
[![codecov](https://codecov.io/gh/jai-python3/jps-cookiecutter-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/jai-python3/jps-cookiecutter-utils)

## 🚀 Overview

**jps-cookiecutter-utils** is a Python-based bootstrapping utility designed to create new code
repositories with a standardized structure, metadata, and configuration files.  
It automates directory creation, file copying, placeholder substitution, and logging,
ensuring uniformity across all your projects.

---

## ✨ Features

- 🚀 Bootstrap new projects from a unified `templates/` directory
- 📁 Create consistent directory layouts automatically
- 🧩 Replace placeholders in files using CLI or input file values
- 🧠 Interactive prompts for missing fields
- 🪵 Comprehensive logging with separated INFO/WARNING levels
- 🎨 Emoji-based verbose progress display
- ⚙️ Typer-powered CLI for intuitive commands

---

## 🧰 Example Usage

```bash
python src/scripts/bootstrap.py \
  --outdir . \
  --code-repository jps-azure-utils \
  --author "Jaideep Sundaram" \
  --author-email jai.python3@gmail.com \
  --code-repo-org jai-python3 \
  --code-repo-summary "Utilities for interacting with Microsoft Azure services." \
  --infile bootstrap.txt \
  --verbose
```

This command creates a new project under `./jps-azure-utils/` with all template files properly substituted.

---

## 📦 Installation

```bash
make install
```

---

## 🧪 Development

```bash
make install-build-tools
make fix && make format && make lint
make test
```

For detailed developer documentation, see [README_DEV.md](./README_DEV.md).

---

## 📜 License

MIT License © Jaideep Sundaram
