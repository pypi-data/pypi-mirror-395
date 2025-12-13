<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/dhruv/main/dhruv_logo.png" alt="dhruv logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/dhruv.svg)](https://pypi.org/project/dhruv/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/dhruv.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/dhruv/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/dhruv/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/dhruv/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/dhruv/graph/badge.svg)](https://codecov.io/gh/dhruv13x/dhruv)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/dhruv/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/dhruv.svg)
[![PyPI Downloads](https://img.shields.io/pypi/dm/dhruv.svg)](https://pypistats.org/packages/dhruv)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/dhruv.svg)](https://pypi.org/project/dhruv/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Docs -->
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://your-docs-link)

</div>

# dhruv 🐍

A foundational Python package for AI-assisted development, designed for simplicity and extensibility.

## About
Dhruv is more than just a template; it's a **"batteries-included" foundation** for building robust Python tools. It comes pre-packaged with an **AI Developer Handbook**—a set of system prompts used to standardize documentation, roadmapping, testing, and refactoring—along with ready-to-use configuration templates.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation
For a straightforward installation, run the following command in the root directory:
```bash
pip install .
```
For developers who wish to modify the source code, install it in editable mode:
```bash
pip install -e .
```

### Usage Example
Verify the installation with the built-in CLI:

```bash
dhruv hello
# Expected Output: "Hello from Dhruv!"
```

---

## ✨ Key Features
- **AI Developer Handbook**: Includes a comprehensive set of system prompts (`src/dhruv/prompts/`) to guide AI agents through Documentation, Roadmapping, Testing, and Refactoring.
- **Batteries-Included Templates**: Pre-configured templates for `pytest` and project settings (`src/dhruv/templates/`).
- **Modern CLI Foundation**: Built with **Typer** and **Rich** for a robust and beautiful command-line interface.
- **Clean Architecture**: Standardized `src` layout ready for expansion.

---

## ⚙️ Configuration & Advanced Usage

### CLI Reference

| Command | Description |
| :--- | :--- |
| `dhruv hello` | Prints a hello message to verify the installation. |

### Accessing Resources
The package includes valuable resources for development:
- **Prompts**: Located in `src/dhruv/prompts/`. Use these to guide your AI coding assistant.
- **Templates**: Located in `src/dhruv/templates/`. Copy these to your project root for instant configuration.

---

## 🏗️ Architecture
The project follows a modular `src` layout:

```text
src/
└── dhruv/
    ├── prompts/    # 📘 AI Developer Handbook & System Prompts
    ├── templates/  # 🛠️ Configuration Templates (pytest, settings)
    ├── utils/      # 🔧 Utility modules (banners, themes)
    ├── cli.py      # 🚀 CLI entry point (Typer)
    └── main.py     # 🧠 Core logic
```

---

## 🗺️ Roadmap
- [x] Initial Release
- [x] Add more utility functions
- [x] Implement a command-line interface
- [ ] Expose prompts and templates via CLI (e.g., `dhruv init`)

---

## 🤝 Contributing & License
Contributions are welcome! Please feel free to submit a pull request.

This project is licensed under the MIT License. See the `pyproject.toml` file for details.
