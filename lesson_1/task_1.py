"""Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление
в формат Unicode и также проверить тип и содержимое переменных."""


def generate_string(word):
    this_string = str(word)
    return f'{this_string} = {type(this_string)}'


def main():
    words = ['разработка', 'сокет', 'декоратор']
    words_unicode = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0441\u043e\u043a\u0435\u0442',
                     '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
    for item in words:
        print(generate_string(item))

    for item in words_unicode:
        print(generate_string(item))


if __name__ == '__main__':
    main()
