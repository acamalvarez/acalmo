# Gemini CLI Project Instructions: acalmo

This document provides specialized mandates for Gemini CLI when working on the **acalmo** Django project. These instructions take precedence over general defaults.

## 🛠 Tech Stack & Environment
- **Framework:** Django 5.2.8
- **Package Manager:** `uv` (Always use `uv add`, `uv remove`, and `uv run`)
- **Python Version:** 3.13+
- **Environment Variables:** Managed via `.env` and `django-environ`. Never commit `.env`.
- **Database:** PostgreSQL (via `psycopg`). Use `python manage.py migrate` for schema updates.

## 📂 Project Structure & Conventions

### 1. Models Organization
- Models in the `portfolio` app are split into multiple files within `portfolio/models/`.
- **Convention:** When adding a new model, create a new file in `portfolio/models/` following the `[topic]_models.py` naming pattern and ensure it is imported in `portfolio/models/__init__.py`.

### 2. Testing
- Tests are located in `portfolio/tests/`.
- **Mandate:** Every logic change or new feature MUST include a corresponding test file or case in `portfolio/tests/`.
- **Run Command:** `uv run python manage.py test portfolio.tests`

### 3. Static & Media Files
- **Static:** Development files are in `static/`. Collected files go to `staticfiles/`.
- **Media:** Local development uses the `media/` directory.
- **Production:** Uses Google Cloud Storage (configured in `settings.py`).
- **Mandate:** When modifying CSS or JS, remind the user to run `python manage.py collectstatic` if they are testing in a production-like environment.

### 4. Code Style
- Use **Type Hints** for all new functions and methods.
- Follow **PEP 8** strictly.
- Use Django's `gettext_lazy` for any user-facing strings (Internationalization is enabled).

## 🚀 Common Workflows

### Dependency Management
- To add a package: `uv add <package>`
- To run a management command: `uv run python manage.py <command>`

### Database Migrations
- Always check for model changes: `uv run python manage.py makemigrations`
- Apply migrations: `uv run python manage.py migrate`

### Development Server
- Run with: `uv run python manage.py runserver`

## ✅ Definition of Done
A task is considered complete only when:
1.  Code is implemented according to the architectural patterns of the project.
2.  Tests are added/updated and passing (`uv run python manage.py test`).
3.  Migrations are generated if models were modified.
4.  No secrets or sensitive data are exposed.
5.  The implementation is verified against the original request.
