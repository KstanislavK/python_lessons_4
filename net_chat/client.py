import argparse
import json
import logging
import socket
import sys
import time
import logs.config_client_log

from decos import log
from common.params import PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_ADDRESS, DEFAULT_PORT
from common.errors import ReqFieldMissingError
from common.utils import send_message, get_message

logger = logging.getLogger('client')


@log
def create_presence(account_name='Klava'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def get_answer(message):
    logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def get_args():
    """Собираем параметры из CMD"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    parser = get_args()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Неверный порт: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    logger.info(f'Подключен клиент: адрес сервера: {server_address}, порт: {server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = get_answer(get_message(transport))
        logger.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        logger.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                        f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()