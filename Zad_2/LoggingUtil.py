import logging
import functools


def get_logger():
    return logging.getLogger(__name__)


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
