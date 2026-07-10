import requests
from config import API_URL
from logger import logger


def token_is_valid(token):
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"Token validation failed: {e}")
        return False


def register(data):
    logger.info("Calling Register API")
    response = requests.post(f"{API_URL}/auth/register", json=data)
    if response.status_code != 201:
        logger.error(f"Register API failed: {response.text}")
    return response


def login(data):
    logger.info("Calling Login API")
    response = requests.post(f"{API_URL}/auth/login", json=data)
    if response.status_code != 200:
        logger.error(f"Login API failed: {response.text}")
    return response


def get_current_user(headers):
    response = requests.get(f"{API_URL}/auth/me", headers=headers)
    if response.status_code != 200:
        logger.error(f"Get Current User API failed: {response.text}")
    return response


def deposit(data, headers):
    logger.info("Calling Deposit API")
    response = requests.post(f"{API_URL}/deposit", json=data, headers=headers)
    if response.status_code != 200:
        logger.error(f"Deposit API failed: {response.text}")
    return response


def withdraw(data, headers):
    logger.info("Calling Withdraw API")
    response = requests.post(f"{API_URL}/withdraw", json=data, headers=headers)
    if response.status_code != 200:
        logger.error(f"Withdraw API failed: {response.text}")
    return response


def balance(headers):
    response = requests.get(f"{API_URL}/balance", headers=headers)
    if response.status_code != 200:
        logger.error(f"Balance API failed: {response.text}")
    return response


def transaction(headers):
    response = requests.get(f"{API_URL}/transaction", headers=headers)
    if response.status_code != 200:
        logger.error(f"Transaction API failed: {response.text}")
    return response


def benefits(headers):
    response = requests.get(f"{API_URL}/benefits", headers=headers)
    if response.status_code != 200:
        logger.error(f"Benefits API failed: {response.text}")
    return response