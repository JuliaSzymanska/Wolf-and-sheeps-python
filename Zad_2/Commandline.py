import argparse
import logging
import os
import Config
import configparser

import LoggingUtil


# todo, poprawić żeby to też logowało? nwm wsm czy to tez

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
        default='DEBUG',
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


# todo, poprawić żeby to też logowało? nwm wsm czy to tez
@LoggingUtil.debug_logging
def configuration(parser):
    # todo rename (logger shadows a name form outer scope, we dont want that)
    args, remainder_argv = parser.parse_known_args()

    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    if args.config:
        config_file = args.config + ".ini"
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

    # todo: dla julki, sprawdz czy to dziala tak jak powinno
    if args.dir:
        Config.SAVE_DIR = args.dir
        Config.SAVE_DIR += '' if Config.SAVE_DIR[-1] == '/' else '/'
        if not Config.SAVE_DIR.startswith('./'):
            Config.SAVE_DIR = './' + Config.SAVE_DIR
        if os.path.exists(Config.SAVE_DIR):
            if not os.path.isdir(args.dir):
                try:
                    os.mkdir(args.dir)
                    Config.SAVE_DIR = args.dir + '/'
                except OSError:
                    raise OSError('Creation of the directory %s failed ' % Config.SAVE_DIR)
                else:
                    raise OSError('Successfully created the directory %s ' % Config.SAVE_DIR)
        else:
            Config.SAVE_DIR = Config.DEFAULT_SAVE_DIR

    # todo: trzeba dorobić info i debug, w poleceniu są wytyczne, mamy loggowac info z programi
    if args.log:
        if args.log not in levels.keys():
            raise ValueError('This log level does not exist.')
        else:
            logging_util_logger = LoggingUtil.get_logger()
            logging_util_logger.setLevel(levels[args.log])
            handler = logging.FileHandler(filename=Config.SAVE_DIR + 'chase.log', mode='w')
            handler.setLevel(levels[args.log])
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logging_util_logger.addHandler(handler)
            # todo tu się coś jebie
            # logging.basicConfig(filename=Config.SAVE_DIR + 'chase.log',
            #                     filemode='w',
            #                     level=levels[args.log])

    if args.rounds:
        if args.rounds > 0:
            Config.ROUNDS = args.rounds
        else:
            raise ValueError('Value should be greater than 0.')

    if args.sheep:
        if args.sheep > 0:
            Config.SHEEP = args.sheep
        else:
            raise ValueError('Value should be greater than 0.')

    if args.wait:
        Config.WAIT = True
