import argparse
import json
import logging
import socket
import sys
import logs.config_server_log

from decos import log
from common.errors import IncorrectDataRecivedError

from common.params import ACTION, TIME, USER, DEFAULT_PORT, CONNECTIONS
from common.utils import get_message, send_message

logger = logging.getLogger('server')


@log
def get_client_msg(message):
    """Функция обрабатывает сообщение пользователя и возвращает ответ"""
    logger.debug(f'Получено сообщение: {message}')
    if ACTION in message and TIME in message and USER in message:
        return {'response': 200}
    return {
        'response': 400,
        'error': 'Bad request'
    }


@log
def get_args():
    """Собираем параметры из CMD"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    """Подгружаем параметры или задаем дефолтные"""
    parser = get_args()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка кореектного порта
    if not 1023 < listen_port < 65536:
        logger.critical(f'Неверный порт {listen_port}. Допустимые от 1024 до 65535')
        sys.exit(1)
    logger.info(f'Сервер запущен с портом {listen_port}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        logger.info(f'Установлено соединение с {client_address}')
        try:
            client_message = get_message(client)
            logger.debug(f'Полсучено сообщение: {client_message}')
            print(client_message)
            response = get_client_msg(client_message)
            logger.info(f'Ответ клиенту: {response}')
            send_message(client, response)
            logger.debug(f'Соединение с клиентом {client_address} закрыто')
            client.close()
        except json.JSONDecodeError:
            logger.error(f'Не удалось декодировать Json строку, от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            logger.error(f'От клиента {client_address} приняты некорректные данные. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
