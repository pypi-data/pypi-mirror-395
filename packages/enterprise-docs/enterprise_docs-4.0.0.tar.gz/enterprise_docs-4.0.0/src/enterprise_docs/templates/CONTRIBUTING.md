---

✅ CONTRIBUTING.md

# Contributing Guide

Thank you for your interest in contributing!  
We welcome high-quality contributions that help make this project better for everyone.

This document outlines standards and expectations for contributing code, documentation, tests, and feedback.

---

## 📋 Table of Contents

- Code of Conduct
- Ways to Contribute
- Getting Started
- Branching Model
- Commit Message Guidelines
- Pull Request Process
- Code Style & Quality Standards
- Testing Requirements
- Documentation
- Security & Responsible Disclosure
- Release & Versioning Policy
- Communication & Support

---

## 🧭 Code of Conduct

Participation in this project requires adherence to our  
**[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)**.

---

## 🤝 Ways to Contribute

- Report bugs & issues
- Suggest features & improvements
- Submit pull requests (PRs)
- Improve documentation & examples
- Improve CI or build tooling
- Write or enhance test coverage
- Performance or security improvements

---

## 🚀 Getting Started

### Fork & clone

git clone https://github.com/<your-org>/<repo>.git cd <repo>

### Set up environment

python -m venv .venv source .venv/bin/activate pip install -e ".[dev]"

> Use `uv` or `pip-tools` if available for reproducible environments.

---

## 🌳 Branching Model

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready |
| `dev` | Active development |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `security/*` | Security fixes |
| `docs/*` | Documentation-only changes |

> ✅ Do **not** push directly to `main`.

---

## 📝 Commit Message Policy

We follow **Conventional Commits**:

Format:

<type>(scope?): <summary>

[optional body]

[optional footer]

Example:

feat(cli): add --dry-run flag fix(imports): resolve path edge case docs: add examples test: improve coverage

> Required for changelog automation & semantic versioning.

---

## 🔁 Pull Request Process

### Before submitting a PR

✅ Ensure all tests pass  
✅ Run linting & type checks  
✅ Update documentation if needed  
✅ Squash small commits  
✅ Reference issue numbers (e.g., `Fixes #42`)

### PR Checklist

- [ ] Code follows project style
- [ ] Test coverage added/updated
- [ ] Docs updated
- [ ] CI pipeline green
- [ ] Changelog entry included (if release-impacting)

### PR Review Standards

- PRs must be reviewed by a maintainer  
- Security-impacting PRs require 2 reviewers  
- Changes must be minimal & scoped

---

## ✅ Code Style & Quality Standards

We enforce:

| Tool | Purpose |
|---|---|
| Ruff | Linting & autofix |
| Black | Formatting |
| Mypy | Type-checking |
| Pytest | Testing |
| Pre-commit hooks | Local quality automation |
| Coverage | ≥ 90% target (unless justified) |

Run locally:

ruff check . black . mypy src pytest

---

## 🧪 Testing

- Write clear, deterministic tests
- Cover edge-cases & failure modes
- No skipping security-related tests
- For major changes, include benchmark/perf notes (if relevant)

---

## 📚 Documentation

All new features must include:

📌 README updates  
📌 CLI examples if applicable  
📌 Docstrings & type hints  
📌 API reference where appropriate  

> Use `mkdocs` if docs site exists.

---

## 🔐 Security & Responsible Disclosure

Do **not** file public security issues.

Report security vulnerabilities privately:  
📧 **security@<your-domain>**

Follow **[SECURITY.md](./SECURITY.md)** guidelines.

---

## 🏷️ Release & Versioning

We use **Semantic Versioning**:

- **BREAKING** → major (X.0.0)
- **Features** → minor (0.X.0)
- **Fixes** → patch (0.0.X)

Releases require:

- Passing CI tests
- Signed release tags (if enabled)
- Changelog entry
- Package build verification

Tag release:

git tag -a vX.Y.Z -m "Release vX.Y.Z" git push origin vX.Y.Z

---

## 💬 Communication

- Use GitHub Issues & Discussions
- Keep conversations respectful & focused
- No private support unless explicitly offered

---

## 🙏 Thank You

We appreciate your contribution and effort to maintain a secure, high-quality, and professional open-source ecosystem!

Welcome aboard 🚀

