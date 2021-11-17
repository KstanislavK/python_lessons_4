"""Создать текстовый файл test_file.txt,
заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое."""


def create_file(lines):
    with open('test_file.txt', 'w', encoding='utf-8') as f:
        for item in lines:
            f.write(f'{item}\n')
        print(f)


def open_file_unicode(file):
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            print(line)


def main():
    lines = ['сетевое программирование', 'сокет', 'декоратор']
    create_file(lines)
    open_file_unicode('test_file.txt')


if __name__ == '__main__':
    main()
