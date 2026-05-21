# FinAdvisor

> Production-ready personal finance advisory platform built with FastAPI, PostgreSQL, SQLAlchemy (async), Alembic, and vanilla HTML/CSS/JS.

FinAdvisor is an advisory-only platform that helps users track income, expenses, debts, and financial goals. It provides AI-assisted insights without any payment processing. Card numbers are never stored in full — only the last 4 digits are retained.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Deployment (Render)](#deployment-render)
- [Notes](#notes)

---

## Features

- User authentication with JWT
- Income and expense tracking
- Debt management (stores only last 4 digits of card numbers)
- Financial goal setting and progress tracking
- Advisory insights and recommendations
- RESTful API under `/api/v1`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL |
| ORM | SQLAlchemy (async) |
| Migrations | Alembic |
| Frontend | Vanilla HTML / CSS / JS |
| Auth | JWT (JSON Web Tokens) |
| Server | Uvicorn |

---

## Prerequisites

Make sure you have the following installed:

- Python 3.11 — [Download](https://www.python.org/downloads/)
- PostgreSQL — [Download](https://www.postgresql.org/download/)
- Git — [Download](https://git-scm.com/)

---

## Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/Spoorthi2603/FinAdvisor_V1.git
cd FinAdvisor_V1
```

**2. Create and activate a virtual environment**

```bash
py -3.11 -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and update the following:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/finadvisor

# Security
SECRET_KEY=your_random_secret_key_here
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=True
```

**Never commit your `.env` file.** It is already listed in `.gitignore`.

To generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Setup

FinAdvisor uses PostgreSQL with async SQLAlchemy. Follow these steps to set up the database locally.

**1. Create the database in PostgreSQL**

Open your PostgreSQL shell (psql) and run:

```sql
CREATE DATABASE finadvisor;
CREATE USER finadvisor_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE finadvisor TO finadvisor_user;
```

**2. Update DATABASE_URL in your `.env`**

```env
DATABASE_URL=postgresql+asyncpg://finadvisor_user:yourpassword@localhost:5432/finadvisor
```

**3. Run Alembic migrations**

This creates all the required tables:

```bash
alembic upgrade head
```

**To create a new migration** after changing models:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

**To roll back the last migration:**

```bash
alembic downgrade -1
```

---

## Running the App

Start the development server:

```bash
uvicorn main:app --reload
```

The app will be available at `http://localhost:8000`.

Interactive API docs are at `http://localhost:8000/docs`.

---

## API Reference

All programmatic endpoints are available under `/api/v1`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| GET | `/api/v1/transactions` | List all transactions |
| POST | `/api/v1/transactions` | Create a transaction |
| GET | `/api/v1/goals` | List financial goals |
| POST | `/api/v1/goals` | Create a financial goal |
| GET | `/api/v1/advisory` | Get financial advisory insights |

Full interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

---

## Project Structure

```
FinAdvisor/
├── main.py                  # App entry point
├── requirements.txt         # Python dependencies
├── alembic.ini              # Alembic configuration
├── .env.example             # Example environment variables
├── alembic/
│   ├── env.py               # Alembic async setup
│   └── versions/            # Migration files
├── app/
│   ├── api/
│   │   └── v1/              # API route handlers
│   ├── core/
│   │   ├── config.py        # Settings from environment
│   │   └── security.py      # JWT and password hashing
│   ├── db/
│   │   ├── base.py          # SQLAlchemy base
│   │   └── session.py       # Async database session
│   ├── models/              # SQLAlchemy ORM models
│   └── schemas/             # Pydantic request/response schemas
└── static/                  # Frontend HTML/CSS/JS
```

---

## Deployment (Render)

### 1. Create a PostgreSQL database on Render

Go to Render Dashboard → New + → PostgreSQL → create a free database. Copy the **Internal Database URL**.

### 2. Create a Web Service on Render

- Connect your GitHub repository
- Set **Runtime** to Python 3
- Set **Build Command**:
  ```
  pip install -r requirements.txt && alembic upgrade head
  ```
- Set **Start Command**:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### 3. Set Environment Variables on Render

In your web service → Environment tab, add:

| Key | Value |
|---|---|
| `DATABASE_URL` | Internal Database URL from step 1 (replace `postgresql://` with `postgresql+asyncpg://`) |
| `SECRET_KEY` | A long random string |
| `JWT_SECRET` | A long random string |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `DEBUG` | `False` |

### 4. Deploy

Push to your `main` branch — Render auto-deploys on every push.

```bash
git add .
git commit -m "your message"
git push origin main
```

---

## Notes

- This is an **advisory-only** platform. No payment processing is included.
- Card numbers are **never stored in full** — only the last 4 digits are retained.
- Use `/api/v1` endpoints for programmatic access.
- The free tier on Render spins down after inactivity — expect a ~50 second cold start on the first request.