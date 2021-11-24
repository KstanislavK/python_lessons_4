"""Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе."""


def encoding_strings(words):
    for item in words:
        try:
            item.encode('ascii')
        except UnicodeEncodeError:
            print(f'Слово "{item}" невозможно записать в байтах')


def main():
    words = ['attribute', 'класс', 'функция', 'type']
    encoding_strings(words)


if __name__ == '__main__':
    main()
