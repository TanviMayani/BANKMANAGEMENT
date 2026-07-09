# Frontend — Banking System UI

A Streamlit interface for the Banking System API, supporting registration, login, and account operations.

## Structure

```
frontend/
└── app.py       # Full Streamlit app (auth + dashboard)
```

## Setup

1. **Install dependencies** (from the project root, using `uv`):
   ```bash
   uv sync
   ```

2. **Make sure the backend is running first** at `http://127.0.0.1:8000` (see [`backend/README.md`](../backend/README.md)).

3. **Run the app:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

The app will open at `http://localhost:8501`.

## Features

- **Register** — create a new account (savings or current)
- **Login** — authenticate and receive a session token
- **Dashboard**, once logged in:
  - Deposit funds
  - Withdraw funds
  - Check balance
  - View transaction history
  - Check benefits (interest, for savings accounts)
  - Logout

## Session Persistence

Streamlit reruns the script on every interaction and doesn't persist state across a full page refresh by default. This app handles that using `st.query_params`:

- On login, the JWT is stored both in `st.session_state['token']` and in the URL via `st.query_params['token']`.
- On page load, if `st.session_state` has no token but the URL does, the app validates that token against `GET /auth/me` before restoring the session.
- On logout, both `st.session_state` and `st.query_params` are cleared.

> Earlier attempts used `streamlit-cookies-controller`, but it had a race condition on component mounting. `st.query_params` proved to be the more stable approach.

## Configuration

The backend URL is currently hardcoded as `http://127.0.0.1:8000` throughout `app.py`. If you deploy the backend elsewhere, update these URLs accordingly (or refactor into a single `API_BASE_URL` constant — see project root README's roadmap section).

## Notes

- All authenticated requests send the token as `Authorization: Bearer <token>` in request headers.
- Form validation (username/password rules) is enforced on the backend; the frontend surfaces any validation errors returned by the API.