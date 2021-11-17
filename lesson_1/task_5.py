"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице."""
import subprocess


def ping_web(urls):
    for item in urls:
        args = ['ping', item]
        subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in subproc_ping.stdout:
            line = line.decode('cp866').encode('utf-8')
            print(line.decode('utf-8'))


def main():
    urls = ['yandex.ru', 'youtube.com']
    ping_web(urls)


if __name__ == '__main__':
    main()
