import argparse
import logging
import select
import socket
import sys
import time

import logs.config_server_log

from decos import log

from common.params import ACTION, TIME, USER, DEFAULT_PORT, CONNECTIONS, MESSAGE_TEXT, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, SENDER, PRESENCE, RESPONSE_200, RESPONSE_400, DESTINATION, EXIT
from common.utils import get_message, send_message

logger = logging.getLogger('server')


@log
def get_client_msg(message, message_list, client, clients, names):
    """Функция обрабатывает сообщение пользователя и возвращает ответ"""
    logger.debug(f'Получено сообщение: {message}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользоватля занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        message_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        logger.info(f'Сообщение для пользователя {message[DESTINATION]} от пользователя {message[SENDER]}')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        logger.error(f'Пользователя {message[DESTINATION]} нет в системе')


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

    names = dict()

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
                    get_client_msg(get_message(client_with_message), messages, client_with_message, clients, names)
                except Exception:
                    logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)
        for item in messages:
            try:
                process_message(item, names, send_data_lst)
            except Exception:
                logger.info(f'Связь с клиентом {item[DESTINATION]} потеряна')
                clients.remove(names[item[DESTINATION]])
                del names[item[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
