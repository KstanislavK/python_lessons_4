import argparse
import logging
import select
import socket
import sys
import time

import logs.config_server_log

from decos import log

from common.params import ACTION, TIME, USER, DEFAULT_PORT, CONNECTIONS, MESSAGE_TEXT, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, SENDER, PRESENCE
from common.utils import get_message, send_message

logger = logging.getLogger('server')


@log
def get_client_msg(message, message_list, client):
    """Функция обрабатывает сообщение пользователя и возвращает ответ"""
    logger.debug(f'Получено сообщение: {message}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and TIME in message and MESSAGE_TEXT in message:
        message_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def get_args():
    """Собираем параметры из CMD"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        logger.critical(f'Неверный порт {listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """Подгружаем параметры или задаем дефолтные"""
    listen_address, listen_port = get_args()
    logger.info(
        f'Запущен сервер с портом: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    transport.listen(CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            logger.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    get_client_msg(get_message(client_with_message), messages, client_with_message)
                except:
                    logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
