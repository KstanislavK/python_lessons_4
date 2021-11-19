"""
Создать текстовый файл test_file.txt,
заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
from chardet import detect


def create_file(lines):
    with open('test_file.txt', 'w') as f:
        for item in lines:
            f.write(f'{item}\n')
    f.close()
    return 'test_file.txt'


def enc_file(new_file):
    with open(new_file, 'rb') as f:
        content = f.read()
        encoding = detect(content)['encoding']
    return encoding


def open_file_unicode(new_file, cod_file):
    with open(new_file, encoding=cod_file) as f:
        lines = f.readlines()
        for line in lines:
            print(line)


def main():
    lines = ['сетевое программирование', 'сокет', 'декоратор']
    new_file = create_file(lines)
    cod_file = enc_file(new_file)
    open_file_unicode(new_file, cod_file)


if __name__ == '__main__':
    main()
