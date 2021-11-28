"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
клиент отправляет запрос серверу; сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
Функции клиента: сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777.
"""

import argparse
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import send_message, get_data_from_message


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

    data = get_data_from_message(sock.recv(1000000))
    print('Сообщение от сервера: ', data)


parser = argparse.ArgumentParser(description='Client arguments')
parser.add_argument('addr', type=str, help='Server address')
parser.add_argument('port', type=int, nargs='*', default=7777, help='server port')
args = parser.parse_args()

s = socket(AF_INET, SOCK_STREAM)
s.connect((args.addr, args.port))
presence(s)

s.close()
