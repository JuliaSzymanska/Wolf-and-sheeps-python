import logging
import functools


def get_logger():
    return logging.getLogger(__name__)


def monitor_results(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        retval = func(*func_args, **func_kwargs)
        logging.getLogger(__name__).debug(
            'function ' + func.__name__ + '() params ' + func_args.__str__() + ' returns ' + repr(retval))
        return retval

    return wrapper
