# Banking System — FastAPI + Streamlit

A full-stack bank management system with JWT-based authentication. The backend is built with **FastAPI** and **PostgreSQL**, and the frontend is a **Streamlit** app that consumes the backend API.

## Project Structure

```
Banking-system-fastapi-streamlit/
├── backend/            # FastAPI REST API
│   ├── auth.py         # Auth routes: register, login, /me
│   ├── config.py       # Centralized settings (.env loader)
│   ├── database.py     # SQLAlchemy engine/session setup
│   ├── main.py         # FastAPI app + banking routes
│   ├── models.py       # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response models
│   ├── security.py     # JWT + password hashing logic
│   ├── scripts/
│   │   └── generate_secret.py
│   └── .env             # Environment variables (not committed)
├── frontend/
│   └── app.py           # Streamlit UI
├── pyproject.toml
├── uv.lock
└── README.md             # (this file)
```

See [`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md) for setup details specific to each part.

## Features

- User registration with validated username/password rules
- JWT-based login and session authentication
- Deposit and withdraw funds
- Check account balance
- View transaction history
- Savings account interest ("benefits") calculation
- Persistent login across Streamlit refreshes using `st.query_params`

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| Auth | JWT (`python-jose`), `passlib`/`bcrypt` |
| Frontend | Streamlit |
| Package management | `uv` |

## Prerequisites

- Python 3.11+
- PostgreSQL running locally (or update `DATABASE_URL` to point elsewhere)
- [`uv`](https://docs.astral.sh/uv/) installed

## Quick Start

1. **Clone the repo and install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up the database.** Create a PostgreSQL database named `bankmanagement` (or update the connection string).

3. **Configure environment variables.** Create a `backend/.env` file — see [`backend/README.md`](backend/README.md) for the required keys.

4. **Run the backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   API docs available at `http://127.0.0.1:8000/docs`.

5. **Run the frontend** (in a separate terminal):
   ```bash
   cd frontend
   streamlit run app.py
   ```
   App available at `http://localhost:8501`.

## How Authentication Works

1. User registers via `/auth/register` — password is hashed with bcrypt before storing.
2. User logs in via `/auth/login` — backend verifies credentials and returns a JWT containing the username and account number.
3. Streamlit stores the token in `st.session_state` and also mirrors it into `st.query_params`, so the session survives a page refresh.
4. Every subsequent request (deposit, withdraw, balance, etc.) sends the token as a `Bearer` token in the `Authorization` header.
5. The backend validates the token on each protected route via `get_current_user` in `security.py`.

## Roadmap Ideas

- Move hardcoded API base URL (`http://127.0.0.1:8000`) in the frontend into a config/env variable
- Add refresh tokens / token expiry handling in the UI
- Add automated tests for auth flow
- Dockerize backend + frontend for easier local setup

## License

Add your license here.