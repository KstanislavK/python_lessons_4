from ipaddress import ip_address
import platform
from pprint import pprint
from subprocess import Popen, PIPE

result = {'Доступные узлы': "", "Недоступные узлы": ""}


def check_ip(value):
    try:
        address = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return address


def host_ping(ip_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for item in ip_list:
        try:
            address = check_ip(item)
        except Exception as e:
            print(f'{item} - {e} воспринимаю как доменное имя')
            address = item

        args = ['ping', param, '1', str(address)]
        reply = Popen(args, stdout=PIPE)
        if reply.wait() == 0:
            result["Доступные узлы"] += f"{str(address)}\n"
            res_string = f"{str(address)} - Узел доступен"
        else:
            result["Недоступные узлы"] += f"{address}\n"
            res_string = f"{str(address)} - Узел недоступен"
        print(res_string)
    return result


if __name__ == '__main__':
    ip_list = ['yandex.ru', '8.8.8.8', '192.168.0.1', 'mail.ru', '80.78.244.143']
    host_ping(ip_list)
    pprint(result)
