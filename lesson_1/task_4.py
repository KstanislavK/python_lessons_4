"""Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode)."""


def encoding_str(words):
    encoded_words = []
    for item in words:
        enc_str = item.encode('utf-8')
        encoded_words.append(enc_str)
    return encoded_words


def decoding_str(dec_words):
    decoded_words = []
    for item in dec_words:
        dec_str = item.decode('utf')
        decoded_words.append(dec_str)
    return decoded_words


def main():
    words = ['разработка', 'администрирование', 'protocol', 'standard']
    print(encoding_str(words))
    print(decoding_str(encoding_str(words)))


if __name__ == '__main__':
    main()
