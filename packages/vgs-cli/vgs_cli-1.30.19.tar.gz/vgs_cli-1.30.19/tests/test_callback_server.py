import requests
import threading
import pytest

from vgscli.callback_server import RequestServer

host = "localhost"
port = 8080
server = RequestServer(host, port)


class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        server.run()


def test_validate_access_token():
    thread = ServerThread()
    thread.daemon = True
    thread.start()

    payload = {"code": "fakeCode"}
    requests.get(__get_host(), params=payload)
    server.close()


def __get_host():
    return "http://" + host + ":" + str(port)
