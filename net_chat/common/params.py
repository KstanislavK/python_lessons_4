import logging

DEFAULT_PORT = 8888
DEFAULT_IP_ADDRESS = '127.0.0.1'
ENCODING = 'utf-8'
LOGGING_LEVEL = logging.DEBUG
CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 1024

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'

MESSAGE = 'message'
MESSAGE_TEXT = 'some text in message'
EXIT = 'exit'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
