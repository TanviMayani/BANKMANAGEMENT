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
├── .env             # Environment variables (git-ignored)
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

---

## Configuration

### Environment Variables

Create `frontend/.env` with:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `API_URL` | Backend API base URL | Yes | `http://127.0.0.1:8000` |
| `STREAMLIT_DEBUG` | Enable debug mode | No | `false` |

### Frontend Configuration (config.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Load from environment, raise error if not set
API_URL = os.getenv("API_URL")
if not API_URL:
    raise ValueError("API_URL environment variable is not set")

STREAMLIT_DEBUG = os.getenv("STREAMLIT_DEBUG", "false").lower() == "true"
```

---

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

## Error Handling

The application gracefully handles:

| Error | Response |
|-------|----------|
| Backend unreachable | Shows error message with connection details |
| Invalid credentials | Displays validation error from backend |
| Invalid token | User redirected to login |
| Expired token | Session cleared, user logged out |
| Network error | Shows connection error message |
| Insufficient funds | Shows error "not enough funds" |
| Invalid amount | Shows validation error |

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

---

## Troubleshooting

### Backend Connection Issues

**Error:** `ConnectionRefusedError: Failed to establish connection`
- **Cause:** Backend not running
- **Solution:** Start backend first
  ```bash
  cd backend
  uv run uvicorn src.main:app --reload
  ```

### Invalid API URL

**Error:** `Failed to validate token` or connection timeouts
- **Cause:** Wrong `API_URL` in `.env`
- **Solution:** Verify backend URL and update `API_URL` in `frontend/.env`

### Token Expiration

**Error:** Suddenly logged out
- **Cause:** JWT token expired after 30 minutes
- **Solution:** Login again

### Environment Variables Not Loading

**Error:** `ValueError: API_URL environment variable is not set`
- **Cause:** `.env` file missing or invalid
- **Solution:** 
  ```bash
  cp .env.example .env
  # Edit .env with correct API_URL
  ```

### Streamlit Caching Issues

**Solution:** Clear Streamlit cache
```bash
streamlit cache clear
```

---

## Development

### Running with Debug Mode

Set in `frontend/.env`:
```env
STREAMLIT_DEBUG=true
```

### Hot Reload
Streamlit automatically reloads when files change. No need to restart.

### Testing in Streamlit
Use the ▶ **Run** button at top-right to re-run after making changes.

---

## Deployment Considerations

For production deployment:
1. Update `API_URL` to production backend
2. Use HTTPS for secure connections
3. Set `STREAMLIT_DEBUG=false`
4. Consider using Streamlit Cloud or self-hosted option
5. Configure proper SSL certificates

---

## Future Enhancements

- [ ] Transaction search and filtering
- [ ] Export transaction history to CSV
- [ ] Account settings page
- [ ] Password change functionality
- [ ] Account transfer between users
- [ ] Push notifications for transactions
- [ ] Dark mode support
- [ ] Mobile responsiveness
- [ ] Profile customization
- [ ] Multi-language support