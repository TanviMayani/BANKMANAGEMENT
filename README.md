# 🏦 Banking Management System

A full-stack Banking Management System built with **FastAPI**, **Streamlit**, and **PostgreSQL**. The application provides secure user authentication using JWT and allows users to perform common banking operations through a simple web interface.

---

## Project Structure

```text
Banking-system-fastapi-streamlit/
│
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── scripts/
│   ├── .env
│   └── README.md
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   ├── api.py
│   ├── config.py
│   └── README.md
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Features

- User Registration
- User Login
- JWT Authentication
- Automatic Account Number Generation
- Deposit Money
- Withdraw Money
- Check Account Balance
- View Transaction History
- Savings Account Benefits
- PostgreSQL Database
- Streamlit Dashboard

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Passlib (bcrypt)
- Pydantic

### Frontend

- Streamlit
- Requests

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Banking-system-fastapi-streamlit
```

Install dependencies:

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

---

## Run the Backend

Open a terminal:

```bash
cd backend
uv run uvicorn src.main:app --reload
```

Backend will start at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Run the Frontend

Open another terminal:

```bash
cd frontend
streamlit run app.py
```

The Streamlit application will open automatically in your browser.

---

## Authentication Flow

1. Register a new account.
2. Login using your username and password.
3. Receive a JWT access token.
4. The frontend stores the token in the session.
5. Every protected request sends:

```
Authorization: Bearer <JWT_TOKEN>
```

6. Logout clears the session and removes the token.

---

## API Overview

### Authentication

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Banking

- `POST /deposit`
- `POST /withdraw`
- `GET /balance`
- `GET /transaction`
- `GET /benefits`

---

## Screens

- Register
- Login
- Dashboard
- Deposit
- Withdraw
- Balance
- Transaction History
- Benefits

---

## Project Modules

### Backend

Handles:

- Authentication
- JWT Token Generation & Validation
- Database Operations
- Banking Business Logic
- REST API Endpoints

See **`backend/README.md`** for backend details.

### Frontend

Handles:

- User Interface
- API Communication
- Session Management
- Dashboard
- Banking Operations

See **`frontend/README.md`** for frontend details.

---

## Developed Using

- Python
- FastAPI
- Streamlit
- PostgreSQL
- SQLAlchemy
- JWT
- Pydantic