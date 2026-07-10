# Frontend — Banking System

A Streamlit-based frontend for the Banking System. It communicates with the FastAPI backend using REST APIs and JWT authentication.

---

## Project Structure

```text
frontend/
├── app.py          # Streamlit user interface
├── api.py          # Functions for API requests
├── config.py       # Backend API configuration
└── __init__.py
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
- Check Account Benefits
- Logout

---

## Requirements

- Python 3.11+
- Streamlit
- Requests

Install dependencies:

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

---

## Configuration
```python
API_URL = "http://127.0.0.1:8501"
```

Update this URL if your backend is running on a different host or port.

---

## Run the Application

### 1. Start the FastAPI backend

```bash
uv run uvicorn backend.src.main:app --reload
```

### 2. Start the Streamlit frontend

```bash
cd frontend
streamlit run app.py
```

---

## Authentication Flow

1. Register a new account.
2. Login using your username and password.
3. The backend returns a JWT access token.
4. The token is stored in the Streamlit session.
5. Every protected API request includes:

```
Authorization: Bearer <JWT_TOKEN>
```

6. Logout clears the session and removes the token.

---

## Technologies Used

- Streamlit
- Python
- Requests
- FastAPI (Backend)
- JWT Authentication

---

## API Endpoints Used

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login user |
| GET | `/auth/me` | Get logged-in user details |
| POST | `/deposit` | Deposit money |
| POST | `/withdraw` | Withdraw money |
| GET | `/balance` | Check account balance |
| GET | `/transaction` | View transaction history |
| GET | `/benefits` | View account benefits |

---

## Notes

- The frontend communicates with the backend using REST APIs.
- JWT is required for all protected operations.
- User sessions are maintained using Streamlit Session State.
- API request functions are organized in `api.py`.
- The backend URL is managed through `config.py`.