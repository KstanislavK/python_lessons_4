import json
import sys

from params import ENCODING, MAX_PACKAGE_LENGTH
from errors import IncorrectDataRecievedError, NonDictInputError

sys.path.append('../')
from decos import log


@log
def get_message(client):
    """Прием и декодирование сообщения"""
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataRecievedError
    else:
        raise IncorrectDataRecievedError


@log
def send_message(sock, message):
    """Кодирования и отправка сообщения"""
    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
