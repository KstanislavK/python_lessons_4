"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице."""
import subprocess
import platform
from chardet import detect


URLS = ['yandex.ru', 'youtube.com']
CODE = '-n' if platform.system() == 'Windows' else '-c'


def ping_web(urls, code):
    for item in urls:
        args = ['ping', code, '4', item]
        subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in subproc_ping.stdout:
            result = detect(line)
            print(result)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


def main():
    ping_web(URLS, CODE)


if __name__ == '__main__':
    main()
