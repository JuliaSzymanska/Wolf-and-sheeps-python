import argparse
import configparser
import logging
import os

from . import Config, LoggingUtil


@LoggingUtil.debug_logging
def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '-c',
        '--config',
        metavar='FILE',
        type=str,
        action='store',
        dest='config',
        help='configuration file name'
    )
    parser.add_argument(
        '-d',
        '--dir',
        metavar='DIR',
        type=str,
        action='store',
        dest='dir',
        help='sub catalogue for storing pos.json and alive.csv files'
    )
    parser.add_argument(
        '-l',
        '--log',
        metavar='LEVEL',
        action='store',
        default='WARNING',
        dest='log',
        type=str,
        help=(
            'enable logging, levels: DEBUG, INFO, WARNING, ERROR, CRITICAL'
            'Example --log DEBUG')
    )

    parser.add_argument(
        '-r',
        '--rounds',
        metavar='NUM',
        type=int,
        dest='rounds',
        action='store',
        help='rounds amount'
    )
    parser.add_argument(
        '-s',
        '--sheep',
        type=int,
        metavar='NUM',
        action='store',
        dest='sheep',
        help='sheep count'
    )
    parser.add_argument(
        '-w',
        '--wait',
        action='store_true',
        dest='wait',
        help='wait after each round of simulation'
    )

    configuration(parser)

    return parser


@LoggingUtil.debug_logging
@LoggingUtil.log_error_exception(OSError)
@LoggingUtil.log_error_exception(ValueError)
@LoggingUtil.log_error_exception(FileNotFoundError)
def configuration(parser):
    args, remainder_argv = parser.parse_known_args()

    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    if args.dir is not None:
        Config.SAVE_DIR = args.dir
        Config.SAVE_DIR += '' if Config.SAVE_DIR[-1] == '/' else '/'
        if not Config.SAVE_DIR.startswith('./'):
            Config.SAVE_DIR = './' + Config.SAVE_DIR
        if not os.path.exists(Config.SAVE_DIR):
            if not os.path.isdir(Config.SAVE_DIR):
                try:
                    os.mkdir(Config.SAVE_DIR)
                except OSError:
                    Config.SAVE_DIR = Config.DEFAULT_SAVE_DIR

    if args.log is not None:
        args.log = args.log.upper()
        if args.log not in levels.keys():
            raise ValueError('This log level does not exist.')
        else:
            LoggingUtil.init_logger(levels[args.log])

    if args.config is not None:
        config_file = args.config
        if not args.config.endswith('.ini'):
            config_file += '.ini'
        if os.path.exists(config_file) and os.path.isfile(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            if float(config['Terrain']['InitPosLimit']) > 0:
                Config.INIT_POS_LIMIT = float(config['Terrain']['InitPosLimit'])
            else:
                raise ValueError('InitPosLimit should be greater than 0.')
            if float(config['Movement']['SheepMoveDist']) > 0:
                Config.SHEEP_MOVE_DIST = float(config['Movement']['SheepMoveDist'])
            else:
                raise ValueError('SheepMoveDist should be greater than 0.')
            if float(config['Movement']['WolfMoveDist']) > 0:
                Config.WOLF_MOVE_DIST = float(config['Movement']['WolfMoveDist'])
            else:
                raise ValueError('WolfMoveDist should be greater than 0.')
        else:
            raise FileNotFoundError('File does not exist')

    if args.rounds is not None:
        if args.rounds > 0:
            Config.ROUNDS = args.rounds
        else:
            raise ValueError('Value should be greater than 0.')

    if args.sheep is not None:
        if args.sheep > 0:
            Config.SHEEP = args.sheep
        else:
            raise ValueError('Value should be greater than 0.')

    if args.wait is not None:
        Config.WAIT = True
