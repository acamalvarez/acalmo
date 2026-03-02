# Acalmo

A professional portfolio website built with Django to showcase projects, skills, and experience.

## Features

- **Project Showcase**: Display featured work with descriptions and links.
- **Experience Timeline**: Sections for Education and Work experience.
- **Skills Management**: Track technical skills with automatically calculated years of experience.
- **Publications**: List and link to articles or research.
- **Contact System**: Integrated contact form with database storage and email notifications.
- **SEO Ready**: Includes sitemaps and robots.txt.
- **Modern Tooling**: Containerized with Docker and managed with `uv`.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Containerization**: Docker & Docker Compose
- **Deployment**: Google Cloud Build ready

## Getting Started

### Prerequisites

- [Python 3.13+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (optional, for containerized development)

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd acalmo
   ```

2. **Install dependencies**:
   Using `uv`:
   ```bash
   uv sync
   ```

3. **Apply migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   uv run python manage.py runserver
   ```

### Running with Docker

You can also run the entire stack using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

## Testing

Run the test suite using:

```bash
uv run python manage.py test
```

## Deployment

This project includes a `cloudbuild.yaml` for automated deployments via Google Cloud Build. Ensure your environment variables (like `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`) are properly configured in your deployment environment.
