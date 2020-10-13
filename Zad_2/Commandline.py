import argparse
import logging


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '-c',
        '--config',
        metavar='FILE',
        type=str,
        action='store',
        help='configuration file name'
    )
    parser.add_argument(
        '-d',
        '--dir',
        metavar='DIR',
        type=str,
        action='store',
        help='sub catalogue for storing pos.json and alive.csv files'
    )
    parser.add_argument(
        '-l',
        '--log',
        metavar='LEVEL',
        action='store',
        default='DEBUG',
        type=str,
        help=(
            'enable logging, levels: DEBUG, INFO, WARNING, ERROR, CRITICAL'
            'Example --log DEBUG')
    )
    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    parser.add_argument(
        '-r',
        '--rounds',
        metavar='NUM',
        type=int,
        action='store',
        help='rounds amount'
    )
    parser.add_argument(
        '-s',
        '--sheep',
        type=int,
        metavar='NUM',
        action='store',
        help='sheep count'
    )
    parser.add_argument(
        '-w',
        '--wait',
        action='store_true',
        help='wait after each round of simulation'
    )
    return parser