"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
item, quantity, price, buyer, date
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    new_order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('orders.json', 'r', encoding='utf-8') as f:
        line = json.load(f)
        order_list = line['orders']
        order_list.append(new_order)

    with open('orders.json', 'w', encoding='utf-8') as ff:
        json.dump(line, ff, indent=4)

        print(line)


item = input('Input item: ')
quantity = input('Input quantity: ')
price = input('Input price: ')
buyer = input('Input buyer: ')
date = input('Input date: ')

write_order_to_json(item, quantity, price, buyer, date)
