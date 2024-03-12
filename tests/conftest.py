import pytest
import requests
import logging
from generate_token import TokenGenerator

TOKEN = TokenGenerator.generate_new_token()

# Initialize logging configuration
logging.basicConfig(filename="tests.log", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture(scope="session")
def no_auth_session():
    with requests.Session() as session:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        session.headers.update(headers)
        yield session


@pytest.fixture(scope="session")
def auth_session():
    with requests.Session() as session:
        token = TOKEN
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': f'token={token}'
        }
        session.headers.update(headers)
        yield session
