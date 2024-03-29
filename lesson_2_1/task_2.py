from task_1 import check_ip, host_ping


def host_range_ping():
    while True:
        start_ip = input("Введите начальный адрес: ")
        try:
            ipv4_start = check_ip(start_ip)
            last_oct = int(start_ip.split('.')[3])
            break
        except Exception as e:
            print(e)
    while True:
        end_ip = input("Сколько адресов проверить?: ")
        if not end_ip.isnumeric():
            print("Необходимо ввести число")
        else:
            if (last_oct + int(end_ip)) > 255+1:
                print(f"Можем менять только последний октет {255+1 - last_oct}")
            else:
                break
    host_list = []
    [host_list.append(str(ipv4_start + x)) for x in range(int(end_ip))]
    return host_ping(host_list)


if __name__ == '__main__':
    host_range_ping()
