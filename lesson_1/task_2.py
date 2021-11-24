"""
Каждое из слов «class», «function», «method» записать в байтовом типе
без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
"""


def binary_task(bi_words):
    for item in bi_words:
        elem = eval(f"b'{item}'")
        print(f"{elem} => type: {type(elem)} => len: {len(elem)}")


def main():
    words = ['class', 'function', 'method']
    binary_task(words)


if __name__ == '__main__':
    main()
