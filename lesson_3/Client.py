import argparse
import sys
import time
import logging
import log.Client.client_log_config

from socket import socket, AF_INET, SOCK_STREAM
from lesson_3.common.utils import send_message, get_data_from_message, load_setting

logger = logging.getLogger('client')


def presence(sock):
    msg_presence = {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": "Client",
            "status": "Connect to server"
        }
    }
    send_message(sock, msg_presence)
    try:
        response = sock.recv(1000000)
    except Exception:
        logger.exception('Ошибка приема ответа с сервера')
        sys.exit(1)
    return get_data_from_message(response)


def main():
    SETTINGS = load_setting(is_server=False)
    parser = argparse.ArgumentParser(description='Client arguments')
    parser.add_argument('addr', type=str, nargs='*', default='', help='Server address')
    parser.add_argument('port', type=int, nargs='*', default='', help='server port')
    args = parser.parse_args()

    if not args.addr:
        server_addr = SETTINGS['DEFAULT_IP_ADDRESS']
        logger.warning('АДрес изменен на дрес по умолчанию')
    else:
        server_addr = args.port

    if not args.port:
        server_port = SETTINGS['DEFAULT_PORT']
        logger.warning('Порт изменен на порт по умолчанию')
    else:
        server_port = args.port

    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((server_addr, server_port))
    except ConnectionRefusedError:
        logger.critical('Ошибка подключения к серверу')
        sys.exit(1)
    response = presence(s)
    logger.debug('Сообщение: ', response)
    s.close()


if __name__ == '__main__':
    main()
