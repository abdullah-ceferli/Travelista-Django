# Travelista Django

## Overview

Travelista is a Django travel website with support for user profiles, blog posts, hotels, insurance offers, and private messaging.

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Create a `.env` file in the project root with your local secrets.
4. Run migrations.
5. Start the development server.

## Setup

```powershell
cd d:\Travelista-Django
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file and set local values for the required keys. Example names include:

- `DJANGO_SECRET_KEY`
- `DEBUG`
- `SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_SECRET_KEY`
- `GEMINI_API_KEY`

> Do not commit secrets or `.env` files to version control.

## Database

```powershell
cd django_project
python manage.py migrate
```

## Run the App

```powershell
cd django_project
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Useful Commands

- Start development server:
  ```powershell
  python manage.py runserver
  ```

- Run on a custom host/port:
  ```powershell
  python manage.py runserver 0.0.0.0:8001
  ```

- Cleanup unused media assets:
  ```powershell
  python manage.py cleanup_media
  ```

- Cleanup bin assets:
  ```powershell
  python manage.py cleanup_bin
  ```

- Force cleanup without confirmation:
  ```powershell
  python manage.py cleanup_bin --force
  ```

## Project Structure

- `django_project/main/templates/pages/` — page templates.
- `django_project/main/static/css/` — custom styles.
- `django_project/main/static/js/` — frontend scripts.
- `django_project/main/apiViews.py` — API endpoints.

## Responsive Improvements

This project now includes better cross-device layout support:

- fluid image and media scaling
- adaptive hero section sizing
- navigation wrapping on smaller screens
- more readable typography on mobile and large monitors

## Notes

- Store local secrets in `.env` only.
- Keep README updated when adding new environment variables.
