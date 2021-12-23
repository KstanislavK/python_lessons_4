import inspect
import logging
import sys
import traceback
import logs.config_server_log
import logs.config_client_log

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):
    def log_saver(*args, **kwargs):
        ret = func(*args, **kwargs)
        logger.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return ret
    return log_saver