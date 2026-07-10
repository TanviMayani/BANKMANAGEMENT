import requests
from config import API_URL


def token_is_valid(token):
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def register(data):
    return requests.post(f"{API_URL}/auth/register", json=data)


def login(data):
    return requests.post(f"{API_URL}/auth/login", json=data)


def get_current_user(headers):
    return requests.get(f"{API_URL}/auth/me", headers=headers)


def deposit(data, headers):
    return requests.post(f"{API_URL}/deposit", json=data, headers=headers)


def withdraw(data, headers):
    return requests.post(f"{API_URL}/withdraw", json=data, headers=headers)


def balance(headers):
    return requests.get(f"{API_URL}/balance", headers=headers)


def transaction(headers):
    return requests.get(f"{API_URL}/transaction", headers=headers)


def benefits(headers):
    return requests.get(f"{API_URL}/benefits", headers=headers)