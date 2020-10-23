import logging
import functools


def get_logger():
    return logging.getLogger(__name__)


def monitor_results(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        retval = func(*func_args, **func_kwargs)
        logging.getLogger(__name__).debug('function %s () params %s returns %s', func.__name__, func_args.__str__(),
                                          repr(retval))
        return retval

    return wrapper


def to_moje_info(msg: str):
    logging.getLogger(__name__).info(msg)