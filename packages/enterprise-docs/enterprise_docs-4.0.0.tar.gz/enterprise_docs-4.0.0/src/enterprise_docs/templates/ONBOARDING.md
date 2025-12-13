# 🎉 Welcome to the Project — Contributor Onboarding

Thank you for joining this project!  
This guide helps you get productive quickly.

---

## 🚀 Quick Start

```bash
git clone https://github.com/<ORG>/<REPO>.git
cd <REPO>
make setup           # or: pip install -e ".[dev]"
make test            # optional

> Automation scripts live in Makefile / Taskfile.yml




---

📦 Development Environment

Tool	Purpose

Python ≥ 3.10	Runtime
Ruff / Black	Code format + lint
Mypy	Type checking
Pytest	Testing
Pre-commit	Hooks
Pip-tools	Reproducible deps
MkDocs	Docs system



---

🧩 Repo Structure

src/<package_name>/
tests/
docs/
scripts/
.github/


---

🧪 Dev Workflow

Step	Command

Install	pip install -e ".[dev]"
Run tests	pytest
Lint	ruff check .
Type check	mypy src
Format	black .
Security scan	pip-audit



---

🤝 Collaboration Rules

Follow CODE_OF_CONDUCT.md

Submit PRs with tests + docs

Use conventional commits (cz commit or feat:, fix: etc.)

Draft PR first when unsure

Request review from maintainers (@dhruv13x)



---

📚 Documentation

Section	Location

User Docs	README.md
Internal Docs	DEVELOPER_GUIDE.md
Architecture	ARCHITECTURE.md
Release Process	RELEASES.md



---

🔐 Security

Never commit secrets

Report vulnerabilities privately (SECURITY.md)

Use security checklist in PR templates



---

💬 Where to Ask Questions

GitHub Discussions (recommended)

Issues → question label

PR comments


> No private support unless commercial contract.




---

🎯 Goal

Enable contributors to become maintainers and future leaders in this ecosystem.

Welcome aboard — let's build great software! 🚀

---
