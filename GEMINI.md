# Gemini CLI Project Instructions: acalmo

This document provides specialized mandates for AI coding assistants (like Gemini CLI) when working on the **acalmo** Django project. These instructions take precedence over general defaults.

## 🎯 Project Overview
**Acalmo** is a professional portfolio website built with Django to showcase projects, skills, and experience. It includes an experience timeline, skills management, publications, and an integrated contact system.

## 🛠 Tech Stack & Environment
- **Framework:** Django 5.2.8
- **Language:** Python 3.13+ (Strict adherence required)
- **Package Manager:** `uv` (Always prefix commands with `uv run`, e.g., `uv run python manage.py ...` and use `uv add`, `uv remove` for dependencies)
- **Frontend:** HTML5, Vanilla CSS, JavaScript
- **Database:** PostgreSQL (via `psycopg`). Local development can use SQLite via memory DB for testing if specified.
- **Environment Variables:** Managed via `.env` and `django-environ`. **Never commit `.env`.**
- **Containerization:** Docker & Docker Compose
- **Deployment:** Google Cloud Run using Google Cloud Build (`cloudbuild.yaml`)
- **Static/Media Files:** Uses `django-storages` with Google Cloud Storage in production. Local uses `media/` and `staticfiles/`.

## 📂 Project Structure & Conventions

### 1. Models Organization
- Models in the `portfolio` app are split into multiple files within `portfolio/models/`.
- **Convention:** When adding a new model, create a new file in `portfolio/models/` following the `[topic]_models.py` naming pattern and ensure it is imported in `portfolio/models/__init__.py`.

### 2. Testing
- Tests are located in `portfolio/tests/`.
- **Mandate:** Every logic change, bug fix, or new feature MUST include a corresponding test file or case in `portfolio/tests/`. Practice Test-Driven Development (TDD) when appropriate.
- **Run Command:** `uv run python manage.py test`
- **Fallback Test Command (No `.env`):** `DATABASE_URL=sqlite:///:memory: CSRF_TRUSTED_ORIGINS=http://localhost:8000 ALLOWED_HOSTS=* SECRET_KEY=dummy DEBUG=True uv run python manage.py test`

### 3. Static & Media Files
- **Static:** Development files are in `static/`. Collected files go to `staticfiles/`.
- **Media:** Local development uses the `media/` directory.
- **Production:** Uses Google Cloud Storage (configured in `settings.py`).
- **Mandate:** When modifying CSS or JS, remind the user to run `uv run python manage.py collectstatic` if they are testing in a production-like environment. Setting `DEBUG=True` is crucial for correctly serving static files locally during UI testing.

### 4. Code Style & Best Practices
- **Type Hints:** Use strict Type Hints for all new functions and methods.
- **Formatting:** Follow **PEP 8** strictly.
- **I18n:** Use Django's `gettext_lazy` for any user-facing strings (Internationalization is enabled).
- **Diagnostics:** If you encounter a build, dependency, or test failure, diagnose the root cause first before trying to alter the environment. Prioritize solutions involving changing code or tests.
- **Security:** Do not expose any secrets or sensitive data.

## 🚀 Common Workflows & Commands

### Dependency Management
- To add a package: `uv add <package>`
- To remove a package: `uv remove <package>`

### Database Migrations
- Always check for model changes: `uv run python manage.py makemigrations`
- Apply migrations: `uv run python manage.py migrate`

### Development Server
- Run with: `uv run python manage.py runserver`
- If restarting a server, kill any existing process on the port first: `kill $(lsof -t -i :8000) 2>/dev/null || true`

## ✅ Definition of Done
A task is considered complete only when:
1. Code is implemented according to the architectural patterns of the project.
2. Changes are verified using a read-only tool (e.g. `read_file`, `list_files`).
3. Tests are added/updated and passing (`uv run python manage.py test`).
4. Migrations are generated if models were modified.
5. No secrets or sensitive data are exposed.
6. The implementation is verified against the original request.
