import json
import logging
from lesson_3.decos import log


@log
def get_logger(is_server):
    if is_server:
        return logging.getLogger('server')
    else:
        return logging.getLogger('client')


def get_data_from_message(response, is_server=True):
    logger = get_logger(is_server)
    response_str = response.decode('utf-8')
    logger.debug(f'это респонс {response_str}')
    return json.loads(response_str)


@log
def send_message(socket, data_dict, is_server=True):
    logger = get_logger(is_server)
    if isinstance(data_dict, dict):
        data = json.dumps(data_dict)
        logger.debug(f'Сообщение отправлено  {socket}')
        return socket.send(bytes(data, encoding="utf-8"))
    else:
        logger.critical("Некорректный формат сообщения")
        raise TypeError


@log
def load_setting(is_server=True, filename='common/settings.json'):
    logger = get_logger(is_server)

    config_keys = ["DEFAULT_IP_ADDRESS", "DEFAULT_PORT", "MAX_CONNECTION", "MAX_PACKAGE_LENGTH", "USER"]
    if not is_server:
        config_keys.append("DEFAULT_IP_ADDRESS")
    with open(filename, 'r') as file:
        configs = json.load(file)
    for key in config_keys:
        if key not in configs:
            logger.critical(f"В конфигурации отсутсвует ключ: {key}")
            raise ValueError
    return configs


def main():
    print(load_setting(is_server=False, filename='common/settings.json'))


if __name__ == '__main__':
    main()
