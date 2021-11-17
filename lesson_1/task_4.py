"""Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode)."""


class CodingStrings():

    def encoding_str(self, words):
        encoded_words = []
        for item in words:
            enc_str = item.encode('utf-8')
            encoded_words.append(enc_str)
        return encoded_words

    def decoding_str(self, dec_words):
        decoded_words = []
        for item in dec_words:
            dec_str = item.decode('utf')
            decoded_words.append(dec_str)
        return decoded_words


def main():
    words = ['разработка', 'администрирование', 'protocol', 'standard']
    decoder = CodingStrings()
    print(decoder.encoding_str(words))
    print(decoder.decoding_str(decoder.encoding_str(words)))


if __name__ == '__main__':
    main()
