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
│   │   ├── auth.py              # Authentication routes
│   │   ├── config.py            # Configuration and environment variables
│   │   ├── database.py          # Database connection setup
│   │   ├── main.py              # FastAPI app and banking endpoints
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── schemas.py           # Pydantic request/response models
│   │   ├── security.py          # JWT and password handling
│   │   └── logger.py            # Logging configuration
│   ├── scripts/
│   │   └── generate_secret.py   # Utility to generate secret keys
│   └── .env                     # Environment variables (git-ignored)
│
├── frontend/
│   ├── app.py                   # Streamlit UI
│   ├── api.py                   # API client functions
│   ├── config.py                # Frontend configuration
│   ├── .env                     # Environment variables (git-ignored)
│   └── .env.example             # Template for .env
│
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## Features

- ✅ User Registration & Login with JWT Authentication
- ✅ Automatic Account Number Generation (UUID)
- ✅ Deposit & Withdraw Money with validations
- ✅ Check Account Balance with full details
- ✅ View Transaction History (deposits and withdrawals)
- ✅ Account Benefits (1% interest for Savings accounts)
- ✅ Secure Password Hashing (bcrypt)
- ✅ PostgreSQL Database with SQLAlchemy ORM
- ✅ Interactive Streamlit Dashboard

---

## Tech Stack

### Backend
- **FastAPI** — Modern async web framework
- **SQLAlchemy** — ORM for database interactions
- **PostgreSQL** — Relational database
- **JWT (Python-Jose)** — Stateless authentication
- **Passlib + bcrypt** — Secure password hashing
- **Pydantic** — Data validation

### Frontend
- **Streamlit** — Interactive web dashboard
- **Requests** — HTTP client library
- **python-dotenv** — Environment variable management

---

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- `uv` package manager (recommended) or pip

### 1. Clone & Install

```bash
git clone <repository-url>
cd Banking-system-fastapi-streamlit
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 2. Database Setup

Create PostgreSQL database:
```bash
createdb bankmanagement
```

Or using SQL:
```sql
CREATE DATABASE bankmanagement;
```

### 3. Backend Configuration

Create `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/bankmanagement
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure secret key:
```bash
cd backend
python scripts/generate_secret.py
```

Copy the output and set it as `SECRET_KEY` in `backend/.env`.

### 4. Frontend Configuration

Create `frontend/.env`:

```env
API_URL=http://127.0.0.1:8000
STREAMLIT_DEBUG=false
```

### 5. Run Backend

```bash
cd backend
uv run uvicorn src.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`  
API Docs: `http://127.0.0.1:8000/docs`

### 6. Run Frontend (in new terminal)

```bash
cd frontend
uv run streamlit run app.py
```

Frontend opens at: `http://localhost:8501`

---

## API Endpoints Overview

### Authentication Routes (no auth required)
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login and get JWT token
- `GET /auth/me` — Get current user (requires token)

### Banking Routes (require JWT)
- `POST /deposit` — Deposit money
- `POST /withdraw` — Withdraw money
- `GET /balance` — Check balance and account details
- `GET /transaction` — View transaction history
- `GET /benefits` — View account benefits (1% interest for savings)

See [Backend README](backend/README.md) for detailed API documentation.

---

## Authentication Flow

```
1. User registers → Password hashed with bcrypt
                 ↓
2. User logs in → Backend validates credentials
                 ↓
3. Backend returns JWT token
                 ↓
4. Frontend stores token in session
                 ↓
5. All subsequent requests include: Authorization: Bearer <TOKEN>
                 ↓
6. Backend validates token on each request
```

---

## Security Features

- 🔒 Passwords hashed with bcrypt (never stored plaintext)
- 🔐 JWT tokens expire after 30 minutes (configurable)
- 🛡️ All protected endpoints require valid JWT
- ✅ Account numbers are auto-generated UUIDs
- 📝 Environment variables for all secrets (no hardcoded values)
- 🔄 Token validation on every protected request

---

## Environment Variables

### Backend (backend/.env)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SECRET_KEY` | Yes | — | JWT signing key (generate with script) |
| `ALGORITHM` | No | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | Token expiration time |

### Frontend (frontend/.env)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_URL` | Yes | — | Backend API base URL |
| `STREAMLIT_DEBUG` | No | false | Enable debug mode |

**Important:** Never commit `.env` files. Use `.env.example` as template.

---

## Project Modules

### Backend (`backend/`)
- **auth.py** — User registration, login, and authentication endpoints
- **main.py** — Banking operations (deposit, withdraw, balance, transactions, benefits)
- **models.py** — SQLAlchemy models (Account, Transaction)
- **security.py** — JWT token creation/validation and password hashing
- **database.py** — SQLAlchemy engine and session management
- **config.py** — Environment variable loading and settings
- **schemas.py** — Pydantic request/response models

See [Backend README](backend/README.md) for complete documentation.

### Frontend (`frontend/`)
- **app.py** — Streamlit UI with login, registration, and banking operations
- **api.py** — HTTP client functions for backend endpoints
- **config.py** — Frontend configuration with environment variable loading
- **.env.example** — Template for frontend environment variables

See [Frontend README](frontend/README.md) for complete documentation.

---

## Database Models

### Account Table
| Column | Type | Constraints |
|--------|------|-------------|
| account_number | String | PK, UNIQUE (UUID) |
| username | String | UNIQUE, NOT NULL |
| password | String | NOT NULL (bcrypt hashed) |
| holder_name | String | — |
| account_type | String | "savings" or "current" |
| balance | Float | DEFAULT 0 |

### Transaction Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PK, AUTO_INCREMENT |
| account_number | String | FK → Account |
| transaction_type | String | "deposit" or "withdraw" |
| amount | Float | — |

---

## Troubleshooting

### Backend Connection Issues
**Error:** `ConnectionRefusedError`
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `backend/.env`
- Ensure database exists

### Frontend Can't Connect to Backend
**Error:** `Failed to establish connection`
- Start backend first
- Verify `API_URL` in `frontend/.env` matches running backend

### JWT Token Errors
- Tokens expire after 30 minutes → login again
- Ensure `SECRET_KEY` is set in `backend/.env`
- Check Authorization header format: `Bearer <TOKEN>`

---

## Future Enhancements

- [ ] Database migrations (Alembic)
- [ ] Comprehensive unit tests
- [ ] Rate limiting and request throttling
- [ ] Email verification for registration
- [ ] Refresh tokens for extended sessions
- [ ] OAuth2 authentication support
- [ ] Transaction search and filtering
- [ ] Account transfer between users
- [ ] Mobile-responsive UI
- [ ] Docker containerization

---

## Technologies Used

- Python 3.11+
- FastAPI
- Streamlit
- PostgreSQL
- SQLAlchemy
- JWT (Python-Jose)
- Passlib (bcrypt)
- Pydantic
- Uvicorn

---

## License

MIT License — Feel free to use this project!

---

## Support

For issues and questions, please open an issue in the repository.