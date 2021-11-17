"""Каждое из слов «class», «function», «method» записать в байтовом типе
без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных."""


def binary_task(bi_words):
    for item in bi_words:
        print(f"{type(item)} = {item} = len: {len(item)}")


def main():
    words = [b'class', b'function', b'method']
    binary_task(words)


if __name__ == '__main__':
    main()
