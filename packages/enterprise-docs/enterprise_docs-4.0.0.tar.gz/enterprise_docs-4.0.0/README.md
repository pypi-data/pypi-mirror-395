<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/enterprise-docs/main/enterprise-docs_logo.png" alt="enterprise-docs logo" width="200"/>
</div>

<div align="center">

# 🧱 Enterprise Docs

**A unified collection of professional, enterprise-grade documentation templates for your projects — enabling consistent governance, security, and compliance across all repositories.**

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/enterprise-docs.svg)](https://pypi.org/project/enterprise-docs/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/enterprise-docs.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/enterprise-docs/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/enterprise-docs/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/enterprise-docs/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/enterprise-docs/graph/badge.svg)](https://codecov.io/gh/dhruv13x/enterprise-docs)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/enterprise-docs/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/enterprise-docs.svg)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/enterprise-docs.svg)](https://pypi.org/project/enterprise-docs/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Docs -->
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://your-docs-link)

</div>

## About

`enterprise-docs` is a command-line tool that provides a comprehensive suite of professional, enterprise-grade documentation templates. It helps organizations and open-source projects maintain consistency, enforce standards, and streamline compliance across all their repositories. With a single command, you can sync everything from `CODE_OF_CONDUCT.md` to a `SECURITY_RESPONSE_PLAYBOOK.md`.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+

### Installation
```bash
pip install enterprise-docs
```

### Usage Example
To see a list of all available documentation templates, run:
```bash
enterprise-docs list
```

To sync all the templates to a local `./docs` directory, run:
```bash
enterprise-docs sync --to ./docs
```

---

## ✨ Key Features

- **God Level Template Library**: Access over 30 professional templates, including `SECURITY.md`, `GOVERNANCE.md`, and `CHANGELOG.md`.
- **Single Source of Truth**: Standardize documentation across all your projects to ensure consistency and compliance.
- **Effortless Synchronization**: A simple and intuitive CLI lets you sync all templates or specific ones with a single command.
- **Custom Sources**: Use your own local directories as sources for templates, allowing you to manage custom template libraries.
- **Automation-Friendly**: Designed to be easily integrated into your CI/CD pipelines, keeping your documentation perpetually up-to-date.
- **Fully Extensible**: While `enterprise-docs` provides a robust set of templates, you can easily add your own to the collection.

---

## ⚙️ Configuration & Advanced Usage

### CLI Arguments

The `enterprise-docs` CLI offers the following commands and options:

| Command     | Description                                     |
|-------------|-------------------------------------------------|
| `list`      | Lists all available documentation templates.    |
| `sync`      | Copies templates to a specified directory.      |
| `version`   | Displays the installed version of the package.  |

| Option     | Default  | Description                                        |
|------------|----------|----------------------------------------------------|
| `--to`     | `./docs` | The destination directory for the `sync` command.  |
| `--source` | `None`   | (Optional) Custom source directory for templates.  |

To sync a specific template:
```bash
enterprise-docs sync MyTemplate.md
```

To use a custom source directory:
```bash
enterprise-docs sync --source ./my-templates
```

---

## 🏗️ Architecture

The project is structured as follows:

```
.
├── src
│   └── enterprise_docs
│       ├── templates
│       │   ├── ARCHITECTURE.md
│       │   ├── ... (and 30+ other templates)
│       │   └── default_pyproject.toml
│       ├── __init__.py
│       ├── banner.py
│       └── cli.py
├── tests
│   └── ...
└── pyproject.toml
```

The core logic is contained in `cli.py`, which parses the command-line arguments and calls the appropriate functions. The `templates` directory contains all the markdown files that are copied by the `sync` command.

---

## 🗺️ Roadmap

For a detailed view of our future plans, please see the [ROADMAP.md](ROADMAP.md) file.

---

## 🤝 Contributing & License

Contributions are welcome! Please see the `CONTRIBUTING.md` file for more details.

This project is licensed under the MIT License. See the `LICENSE` file for more details.
