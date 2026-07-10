# Frontend — Banking System Dashboard

A Streamlit-based interactive dashboard for the Banking System. Communicates with the FastAPI backend using REST APIs and JWT authentication.

---

## Overview

The frontend provides a user-friendly interface for:
- User registration and login
- Account balance checking
- Deposit and withdrawal operations
- Transaction history viewing
- Account benefits viewing
- Session management with JWT tokens

---

## Project Structure

```text
frontend/
├── app.py           # Main Streamlit application
├── api.py           # API client functions (HTTP requests)
├── config.py        # Configuration and environment loading
├── __init__.py
├── .env             # Environment variables 
└── .env.example     # Template for environment setup
```

---

## Requirements

- Python 3.11+
- Streamlit 1.58+
- Requests
- python-dotenv

Install dependencies:

```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

---

## Setup Instructions

### 1. Create Environment File

Copy the template:
```bash
cp .env.example .env
```

### 2. Configure Backend URL

Edit `frontend/.env`:

```env
API_URL=http://127.0.0.1:8000
STREAMLIT_DEBUG=false
```

**Important Notes:**
- `API_URL` must match your running backend server
- Never commit `.env` file to git

---

## Running the Application

### Prerequisites
- Backend API must be running first (see Backend README)

### Start the Frontend

```bash
cd frontend
uv run streamlit run app.py
```

The app automatically opens in your browser at: `http://localhost:8501`

---

## Application Features

### 1. Authentication

#### Registration
- Create new account with username and password
- Choose account type: **Savings** or **Current**
- Auto-generated account number
- Success confirmation with celebration animation

#### Login
- Authenticate with username and password
- Receive and store JWT token
- Token persisted in session and URL for page refreshes
- Redirect to dashboard on success

#### Logout
- Clear session and remove token
- Redirect to login page

---

### 2. Dashboard

Once logged in, displays:
- **Welcome message** with username
- **Account details:**
  - Account number
  - Account holder name
  - Account type
  - Current balance

---

### 3. Banking Operations

#### Deposit Money
- Enter amount to deposit
- Confirms successful deposit
- Displays updated balance
- Error handling for invalid amounts or server issues

#### Withdraw Money
- Enter amount to withdraw
- Validates sufficient balance
- Confirms successful withdrawal
- Displays updated balance
- Shows error if insufficient funds

#### Check Balance
- View current account balance
- See full account details:
  - Account number
  - Holder name
  - Account type
  - Balance

#### Transaction History
- View all transactions for the account
- Shows transaction type (deposit/withdraw) and amounts
- Displayed in table format
- Shows message if no transactions exist

#### Benefits
- View account-specific benefits
- **Savings Accounts:** 1% annual interest on current balance
- **Current Accounts:** No benefits
- Calculated based on account type and balance

---

## Session Management

### How Sessions Work
1. User logs in and receives JWT token from backend
2. Token stored in Streamlit `session_state`
3. Token also added to URL query parameters
4. On page reload, frontend validates token is still valid
5. If valid, session restored automatically
6. If invalid, redirected to login

### Token Validation
- Tokens sent with every request in `Authorization: Bearer {token}` header
- Backend validates token authenticity and expiration
- Frontend checks if validation response is successful (HTTP 200)
- Expired tokens result in 401 error, user must login again

### Session Timeout
- Tokens expire after 30 minutes (backend setting)
- User automatically redirected to login after expiration
- Re-login required to continue



## API Integration

### API Client (api.py)

The `api.py` file contains wrapper functions for backend endpoints:

```python
# Authentication
token_is_valid(token)              # Validate token
register(data)                     # Register new user
login(data)                        # Login user
get_current_user(headers)          # Get current user info

# Banking Operations
deposit(data, headers)             # Deposit money
withdraw(data, headers)            # Withdraw money
balance(headers)                   # Check balance
transaction(headers)               # Get transaction history
benefits(headers)                  # Get account benefits
```

### Authentication Header Format

```python
headers = {
    "Authorization": f"Bearer {token}"
}
```

---

## User Interface

### Streamlit Features Used
- `st.set_page_config()` — Page configuration
- `st.sidebar.radio()` — Navigation menu
- `st.form()` — Login/register forms
- `st.session_state` — Session management
- `st.query_params` — URL state management
- `st.dataframe()` — Transaction table display
- `st.success()`, `st.error()`, `st.warning()` — Notifications
- `st.balloons()` — Celebration animation

### Page Layout
- **Sidebar:** Navigation menu (only when not logged in)
- **Main area:** Current page content
- **Logout button:** Available in sidebar when logged in

---

## Security

### Authentication
- JWT tokens used for all authenticated requests
- Tokens stored in session (not persistent storage)
- Token included in Authorization header

### Data Protection
- Passwords never sent to frontend
- Never logged or displayed in browser
- All sensitive data from backend

### Frontend Security
- No hardcoded credentials
- Secrets loaded from `.env` (git-ignored)
- HTTPS recommended for production

