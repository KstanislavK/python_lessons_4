import argparse
import time
from json import JSONDecodeError
from socket import AF_INET, socket, SOCK_STREAM
import logging
from decos import log

from common.utils import send_message, get_data_from_message, load_setting

logger = logging.getLogger('server')


@log
def send_success_code(client):
    msg_response = {
        "response": '200',
        "time": int(time.time()),
    }
    send_message(client, msg_response)


@log
def main():
    SETTINGS = load_setting(is_server=False, filename='common/settings.json')
    parser = argparse.ArgumentParser(description='Server arguments')
    parser.add_argument('addr', type=str, nargs='*', default='', help='Clients address')
    parser.add_argument('port', type=int, nargs='*', default='', help='server port')
    args = parser.parse_args()

    if not args.port:
        server_port = SETTINGS["DEFAULT_PORT"]
        logger.warning("Успользуется порт сервера по умолчанию")
    else:
        server_port = args.port

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((args.addr, server_port))
    s.listen(SETTINGS['MAX_CONNECTION'])

    while True:
        client, addr = s.accept()
        try:
            data = get_data_from_message(client.recv(SETTINGS['MAX_PACKAGE_LENGTH']))
            logger.debug(f'Сообщение: {data}, было отправлено клиентом: {addr}')
        except JSONDecodeError:
            logger.exception('Некорректный формат JSON файла')

        send_success_code(client)

        client.close()


if __name__ == '__main__':
    main()
