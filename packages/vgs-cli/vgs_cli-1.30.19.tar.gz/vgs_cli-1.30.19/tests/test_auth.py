import os
import tempfile
import sys
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta

from click.testing import CliRunner
from vgscli.click_extensions import Config

from vgs.sdk.utils import silent_file_remove

from io import StringIO

from vgscli.vgs import cli, login

TEST_JWT_HEADER = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhQmZ2bElkQXR3WHFPUzNxMF9SSnZjd1pkWGtybjBQaWNNZjllRGc3bEhJIn0"
TEST_JWT_PAYLOAD = (
    "eyJqdGkiOiIwNzAxYjEyMy0yN2JmLTRkY2ItYWQ5MS1lMDczNzY4NmUzOWEiLCJleHAiOjE1NDIwMzI5MjcsIm5iZi"
    "I6MCwiaWF0IjoxNTQyMDMyNjI3LCJpc3MiOiJodHRwczovL2F1dGgudmVyeWdvb2RzZWN1cml0eS5jb20vYXV0aC9yZWFsbXMvdmd"
    "zIiwiYXVkIjoidmdzLWNsaSIsInN1YiI6ImVlZnJhc2ZlZ2UtY2EwYS00NTdhLTllOWMtYzIyOGNjMWY2N2IzIiwidHlwIjoiQmVh"
    "cmVyIiwiYXpwIjoidmdzLWNsaSIsImF1dGhfdGltZSI6MCwic2Vzc2lvbl9zdGF0ZSI6IjkyNmE5ZTE2LTVhMzQtNGRiYy1iZDA2L"
    "WRjYTk4MTBlMDJjNyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOltdLCJyZXNvdXJjZV9hY2Nlc3MiOnt9LCJzY29wZSI6IiJ9"
)
TEST_JWT_SIGNATURE = (
    "NTRQlv6-UY-eo4_83QH4WUiS0sYeMFFHtZeGYsjmQF8Kd-Ar1vzjMKRnOH4qHrdfaw3trc4P_Q2uRoXCA3dT4KxSj4FzN0PDo0"
    "9ykwr5RbQbOlzzdZEpjZxeaAZ5A_KalXorCrNOwbuIWMWkencLVIOhkeKRytqz62V6SXt8jIjCQXGT85eTXMdLq5jcppo7Bc5F9Q9"
    "75GBM1G1eojn1njXt0EqyrXDTUgs6TWWjBM4xEi4zxXhcUNXIgpPZQWy7M_1bTVL7uHLcu-PfS-vUs2FCd274DENEV4RYuJ_I6Xys"
    "E8FtPmZog9fB6GoNKAWMMQhycp1lkSbnRtY-beNIhQ"
)
TEST_JWT = "{header}.{payload}.{signature}".format(
    header=TEST_JWT_HEADER, payload=TEST_JWT_PAYLOAD, signature=TEST_JWT_SIGNATURE
)


def __login_twice_assert(mocker, temp_file, now_time, token_calls_count):
    token1 = login(None)
    spy = mocker.spy(auth, "__get_access_token")
    token2 = login(None)

    assert spy.call_count == token_calls_count
    assert token1 == token2 == TEST_JWT
    assert os.path.exists(temp_file) and os.path.isfile(temp_file)


def __login_fake_token(mocker, token_file_name, login_actions):
    temp_file, token_file_name = __create_temp_token_file(token_file_name)
    auth.TOKEN_FILE_NAME = token_file_name

    try:
        with FakeStd():
            mocker.patch("vgscli.auth.__get_access_token", return_value=TEST_JWT)

            login_actions(temp_file)
    finally:
        # clear file
        silent_file_remove(temp_file)


def __create_temp_token_file(filename):
    temp_dir = tempfile.gettempdir()
    token_file_name = filename
    temp_file = os.path.join(temp_dir, token_file_name)
    # make sure there is no file
    silent_file_remove(temp_file)
    return temp_file, token_file_name


class FakeStd(object):
    """
    Mutes std output for tests
    """

    def __init__(self):
        self.stdout = None
        self.stderr = None

    def __enter__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def __exit__(self, type, value, traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr


def generate_jwt(client_id):
    return jwt.encode(
        {"azp": client_id, "exp": datetime.utcnow() + timedelta(seconds=30)},
        "secret",
        algorithm="HS256",
    )


@patch("vgscli.auth.AuthServer")
def test_client_credentials_login(AuthServer):
    os.environ["VGS_CLIENT_ID"] = "CLIENT1"
    os.environ["VGS_CLIENT_SECRET"] = "SECRET1"

    runner = CliRunner()
    # use logout command to trigger CLI auto-login, it might be any other command
    result = runner.invoke(cli, ["logout"], obj=Config(False, "production"))

    os.environ.pop("VGS_CLIENT_ID")
    os.environ.pop("VGS_CLIENT_SECRET")

    assert result.exit_code == 0
    assert AuthServer().client_credentials_login.call_args[0] == ("CLIENT1", "SECRET1")


@patch("vgscli.auth.token_util.is_access_token_valid")
@patch("vgscli.auth.token_util.get_access_token")
@patch("vgscli.auth.AuthServer")
def test_client_credentials_login_new_client_id(
    AuthServer, get_access_token, is_access_token_valid
):
    os.environ["VGS_CLIENT_ID"] = "CLIENT2"
    os.environ["VGS_CLIENT_SECRET"] = "SECRET2"

    get_access_token.return_value = generate_jwt("CLIENT1")
    is_access_token_valid.return_value = True

    runner = CliRunner()
    # use logout command to trigger CLI auto-login, it might be any other command
    result = runner.invoke(cli, ["logout"], obj=Config(False, "production"))

    os.environ.pop("VGS_CLIENT_ID")
    os.environ.pop("VGS_CLIENT_SECRET")

    assert result.exit_code == 0
    assert AuthServer().client_credentials_login.call_args[0] == ("CLIENT2", "SECRET2")
