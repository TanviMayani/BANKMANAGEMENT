# Backend — Banking System API

A FastAPI REST API for a Banking Management System, using PostgreSQL for data storage and JWT (JSON Web Token) for authentication.

---

## Project Structure

```text
backend/
├── src/
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── config.py        # Application configuration
│   ├── database.py      # Database connection and SQLAlchemy setup
│   ├── main.py          # FastAPI application and banking routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic request/response models
│   └── security.py      # JWT authentication and password hashing
│
├── scripts/
│   └── generate_secret.py
│
├── .env
└── README.md
```

---

## Features

- User Registration
- User Login
- JWT Authentication
- Deposit Money
- Withdraw Money
- Check Account Balance
- View Transaction History
- Savings Account Benefits
- PostgreSQL Database Integration

---

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Passlib
- Python-Jose
- Pydantic Settings

Install all dependencies:

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create a PostgreSQL database.

```sql
CREATE DATABASE bankmanagement;
```

---

## Environment Variables

Create a `.env` file inside the `backend` folder.

```env
SECRET_KEY=<your-generated-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://postgres:123@localhost:5432/bankmanagement
```

Generate a secure secret key using:

```bash
python scripts/generate_secret.py
```

Copy the generated value into `SECRET_KEY`.

---

## Run the Backend

From the `backend` directory:

```bash
uv run uvicorn src.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| SECRET_KEY | Yes | — | Secret key used to sign JWT tokens |
| ALGORITHM | No | HS256 | JWT signing algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | 30 | JWT expiration time in minutes |
| DATABASE_URL | Yes | — | PostgreSQL connection string |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and generate JWT | No |
| GET | `/auth/me` | Get logged-in user details | Yes |

### Register Request

```json
{
    "username": "johndoe1",
    "password": "Str0ng!Pass",
    "account_type": "savings"
}
```

### Login Request

```json
{
    "username": "johndoe1",
    "password": "Str0ng!Pass"
}
```

---

### Banking APIs

All endpoints below require an Authorization header.

```
Authorization: Bearer <JWT_TOKEN>
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/deposit` | Deposit money |
| POST | `/withdraw` | Withdraw money |
| GET | `/balance` | Check account balance |
| GET | `/transaction` | View transaction history |
| GET | `/benefits` | Check savings account benefits |

---

## Authentication Flow

1. Register a new account.
2. Login with username and password.
3. A JWT access token is generated.
4. Include the token in the request header:

```
Authorization: Bearer <JWT_TOKEN>
```

5. `get_current_user()` validates the JWT before accessing protected endpoints.

---

## Notes

- Passwords are securely hashed using **bcrypt**.
- JWT tokens contain both the username and account number.
- Account numbers are generated automatically during registration.
- SQLAlchemy automatically creates database tables when the application starts.
- Configuration values are loaded from the `.env` file using **Pydantic Settings**.

---

## Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Passlib (bcrypt)
- Pydantic
- Uvicorn