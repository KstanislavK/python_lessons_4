"""Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе."""


def encoding_strings(words):
    for item in words:
        enc_str = str.encode(item, encoding='utf-8')
        print(enc_str, type(enc_str))


def main():
    words = ['attribute', 'класс', 'функция', 'type']
    encoding_strings(words)


if __name__ == '__main__':
    main()
