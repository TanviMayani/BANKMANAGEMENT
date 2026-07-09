# Backend — Banking System API

A FastAPI REST API for a bank management system, using PostgreSQL for storage and JWT for authentication.

## Structure

```
backend/
├── auth.py         # Auth routes: /auth/register, /auth/login, /auth/me
├── config.py       # Loads and validates environment variables
├── database.py     # SQLAlchemy engine + session setup
├── main.py         # FastAPI app instance + banking routes
├── models.py       # SQLAlchemy ORM models (Account, Transaction)
├── schemas.py      # Pydantic models for requests/responses
├── security.py     # Password hashing, JWT creation/verification, get_current_user
├── scripts/
│   └── generate_secret.py   # One-off script to generate a SECRET_KEY
└── .env             # Environment variables (create this yourself, not committed)
```

## Setup

1. **Install dependencies** (from the project root, using `uv`):
   ```bash
   uv sync
   ```

2. **Create a PostgreSQL database:**
   ```sql
   CREATE DATABASE bankmanagement;
   ```

3. **Generate a secret key:**
   ```bash
   python scripts/generate_secret.py
   ```
   Copy the output into your `.env` file as `SECRET_KEY`.

4. **Create `backend/.env`:**
   ```env
   SECRET_KEY=<your-generated-secret>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=postgresql://postgres:123@localhost:5432/bankmanagement
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be live at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | — | Used to sign JWTs. Generate with `scripts/generate_secret.py`. |
| `ALGORITHM` | No | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | How long a login token stays valid. |
| `DATABASE_URL` | No | local Postgres default | Full PostgreSQL connection string. |

> Note: `config.py` uses `extra = "ignore"`, so unrelated variables in `.env` won't crash the app — but make sure the variable names above match exactly, or your values will silently fall back to defaults.

## API Endpoints

### Auth (`/auth`)

| Method | Path | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register` | Create a new account | No |
| POST | `/auth/login` | Log in, returns a JWT | No |
| GET | `/auth/me` | Get current logged-in user info | Yes |

**Register request body:**
```json
{
  "username": "johndoe1",
  "password": "Str0ng!Pass",
  "account_type": "savings"
}
```
- Username: 4–20 characters, letters/numbers/underscores only
- Password: 8+ characters, must include uppercase, lowercase, number, and special character
- Account type: `savings` or `current`

**Login request body:**
```json
{
  "username": "johndoe1",
  "password": "Str0ng!Pass"
}
```

### Banking (no prefix)

All routes below require a `Bearer` token in the `Authorization` header.

| Method | Path | Description |
|---|---|---|
| POST | `/deposit` | Deposit funds. Body: `{"amount": 100}` |
| POST | `/withdraw` | Withdraw funds. Body: `{"amount": 50}` |
| GET | `/balance` | Get account balance and details |
| GET | `/transaction` | Get transaction history |
| GET | `/benefits` | Get interest info (savings accounts only) |

## Authentication Flow

1. `POST /auth/register` — password hashed with bcrypt, account number auto-generated
2. `POST /auth/login` — verifies password, returns a signed JWT containing `sub` (username) and `account_number`
3. Client sends the token as `Authorization: Bearer <token>` on every protected request
4. `security.get_current_user` decodes and validates the token on each request

## Notes

- `models.Base.metadata.create_all(bind=engine)` in `main.py` auto-creates tables on startup — no separate migration step needed for this project's scale.
- Account numbers are randomly generated 10-digit strings, checked for uniqueness before assignment.