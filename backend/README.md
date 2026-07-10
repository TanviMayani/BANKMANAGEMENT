# Backend — Banking System API

A FastAPI REST API for a Banking Management System using PostgreSQL for data storage and JWT for authentication.

---

## Overview

The backend provides RESTful endpoints for:
- User registration and authentication
- Banking operations (deposit, withdraw, balance check)
- Transaction history tracking
- Account benefits calculation

---

## Project Structure

```text
backend/
├── src/
│   ├── __init__.py
│   ├── auth.py              # Authentication routes (register, login, me)
│   ├── config.py            # Settings and environment loading
│   ├── database.py          # SQLAlchemy setup and session management
│   ├── main.py              # FastAPI app, banking routes (deposit, withdraw, etc)
│   ├── models.py            # ORM models (Account, Transaction)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── security.py          # JWT token handling and password hashing
│   └── logger.py            # Logging configuration
├── scripts/
│   └── generate_secret.py   # Utility to generate secure secret keys
└── .env                     # Environment variables (git-ignored)
```

---

## Requirements

- Python 3.11+
- PostgreSQL 12+
- FastAPI
- SQLAlchemy
- Uvicorn
- Python-Jose (JWT)
- Passlib (password hashing)
- Pydantic
- Pydantic-settings

Install all dependencies:

```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

---

## Setup Instructions

### 1. Environment Configuration

Create `.env` file in `backend/` directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/bankmanagement
SECRET_KEY=your-generated-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Generate Secret Key

```bash
cd backend
python scripts/generate_secret.py
```

Copy the generated key and set it as `SECRET_KEY` in `.env`.

### 3. Database Setup

Create PostgreSQL database:

```bash
createdb bankmanagement
```

Or using psql:
```sql
CREATE DATABASE bankmanagement;
```

The tables will be automatically created when you first run the app (SQLAlchemy `create_all`).

---

## Running the Backend

### Development Server

```bash
cd backend
uv run uvicorn src.main:app --reload
```

The API starts at: `http://127.0.0.1:8000`

### Production Server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## API Documentation

Once running, access interactive docs at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
---

## API Endpoints

### Authentication Routes

#### POST `/auth/register`
Register a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password",
  "account_type": "savings"
}
```

**Response (201):**
```json
{
  "username": "john_doe",
  "account_number": "550e8400-e29b-41d4-a716-446655440000",
  "holder_name": "john_doe",
  "account_type": "savings"
}
```

#### POST `/auth/login`
Login and receive JWT token.

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/auth/me`
Get current authenticated user info.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "account_number": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "holder_name": "john_doe",
  "account_type": "savings",
  "balance": 5000.0
}
```

---

### Banking Routes

All banking endpoints require authentication. Include JWT token in header:
```
Authorization: Bearer {access_token}
```

#### POST `/deposit`
Deposit money to account.

**Request:**
```json
{
  "amount": 1000.0
}
```

**Response (200):**
```json
{
  "message": "amount deposited successfully",
  "current_balance": 6000.0
}
```

**Errors:**
- `400` — Amount must be positive
- `404` — Account not found

---

#### POST `/withdraw`
Withdraw money from account.

**Request:**
```json
{
  "amount": 500.0
}
```

**Response (200):**
```json
{
  "message": "amount withdrawn successfully",
  "current_balance": 5500.0
}
```

**Errors:**
- `400` — Amount must be positive, or insufficient funds
- `404` — Account not found

---

#### GET `/balance`
Check account balance and details.

**Response (200):**
```json
{
  "account_number": "550e8400-e29b-41d4-a716-446655440000",
  "holder_name": "john_doe",
  "account_type": "savings",
  "balance": 5500.0
}
```

**Errors:**
- `404` — Account not found

---

#### GET `/transaction`
View transaction history.

**Response (200):**
```json
[
  {
    "id": 1,
    "account_number": "550e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "deposit",
    "amount": 5000.0
  },
  {
    "id": 2,
    "account_number": "550e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "deposit",
    "amount": 1000.0
  },
  {
    "id": 3,
    "account_number": "550e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "withdraw",
    "amount": 500.0
  }
]
```

**Errors:**
- `400` — Account not found

---

#### GET `/benefits`
View account benefits.

**Response (200) - Savings Account:**
```json
{
  "interest": 55.0
}
```

**Response (200) - Current Account:**
```json
{
  "message": "account type - current - no benefits are there for current account"
}
```

*Note: Savings accounts earn 1% annual interest on current balance.*


## Security

### Password Security
- Passwords are hashed using **bcrypt** via Passlib
- Never stored or logged in plaintext
- Always validated during login

### JWT Tokens
- Tokens expire after 30 minutes (configurable)
- Signed with `SECRET_KEY` using `HS256` algorithm
- Validated on every protected endpoint request

### Account Security
- Account numbers are randomly generated UUIDs
- Each account is isolated to authenticated user
- Balance checks prevent overdraft

### Environment Security
- All secrets stored in `.env` (git-ignored)
- No hardcoded credentials
- `SECRET_KEY` must be generated separately

---





## Development Tips

### Database Inspection
Connect to PostgreSQL and inspect tables:
```bash
psql -d bankmanagement
```

### View API Routes
```bash
python -c "from src.main import app; [print(route.path, route.methods) for route in app.routes]"
```
