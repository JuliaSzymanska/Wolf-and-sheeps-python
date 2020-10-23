import logging
import functools

import Config


def init_logger(level: int):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    handler = logging.FileHandler(filename=Config.SAVE_DIR + 'chase.log', mode='w')
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def debug_logging(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        retval = func(*func_args, **func_kwargs)
        logging.getLogger(__name__).debug('function %s () params %s returns %s', func.__name__, func_args.__str__(),
                                          repr(retval))
        return retval

    return wrapper


def info_logging(message: str):
    logging.getLogger(__name__).info(message)


def warning_logging():
    i = 0
