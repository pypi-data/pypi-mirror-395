import jwt
import time
import pytest

from cryptography.fernet import Fernet
from vgscli.keyring_token_util import KeyringTokenUtil, TokenNotValidError

SERVICE_NAME = "vgs-cli"
ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"
keyring_token_util = KeyringTokenUtil()


def test_validate_access_token():
    __create_signing_secret()
    token = __get_valid_token()
    keyring_token_util.put_access_token(token)
    keyring_token_util.validate_access_token()
    keyring_token_util.delete_access_token()


def test_validate_refresh_token():
    __create_signing_secret()
    token = __get_valid_token()
    keyring_token_util.put_refresh_token(token)
    keyring_token_util.validate_refresh_token()
    keyring_token_util.delete_refresh_token()


def test_validate_invalid_access_token():
    __create_signing_secret()
    token = __get_expired_token()
    keyring_token_util.put_access_token(token)
    assert keyring_token_util.validate_access_token() == False


def test_validate_invalid_refresh_token():
    __create_signing_secret()
    with pytest.raises(TokenNotValidError) as pytest_wrapped_e:
        token = __get_expired_token()
        keyring_token_util.put_refresh_token(token)
        keyring_token_util.validate_refresh_token()
    assert pytest_wrapped_e.type == TokenNotValidError


def test_process_token_response():
    response = {}
    access_token = "access_token"
    refresh_token = "refresh_token"
    response[access_token] = access_token
    response[refresh_token] = refresh_token
    keyring_token_util.put_tokens(response)
    assert keyring_token_util.get_access_token() == access_token
    assert keyring_token_util.get_refresh_token() == refresh_token


def test_delete_refresh_token():
    token = __get_expired_token()
    keyring_token_util.put_refresh_token(token)

    assert keyring_token_util.get_refresh_token() == token

    keyring_token_util.delete_refresh_token()

    with pytest.raises(TokenNotValidError):
        assert keyring_token_util.get_refresh_token() == token


def test_delete_access_token():
    token = __get_expired_token()
    keyring_token_util.put_access_token(token)

    assert keyring_token_util.get_access_token() == token

    keyring_token_util.delete_access_token()

    with pytest.raises(TokenNotValidError):
        assert keyring_token_util.get_access_token() == token


def __get_valid_token():
    return str(jwt.encode({"exp": time.time() + 3600}, "secret", algorithm="HS256"))


def __get_expired_token():
    return str(jwt.encode({"exp": time.time() - 3600}, "secret", algorithm="HS256"))


def __create_signing_secret():
    key = Fernet.generate_key()
    keyring_token_util.put_encryption_secret(str(key, "utf-8"))
