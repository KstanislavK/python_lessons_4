import logging
import os

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

logger = logging.getLogger('client')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
file_handler = logging.FileHandler(PATH, encoding='utf-8')

file_handler .setLevel(logging.INFO)
file_handler .setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info('Тестируем логирование')
