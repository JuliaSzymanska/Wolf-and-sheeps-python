import argparse
import logging
import configparser
import os

CONFIG_FILE = ''
SAVE_DIR = './'
INITPOSLIMIT = 10.0
SHEEPMOVEDIST = 0.5
WOLFMOVEDIST = 1.0
ROUNDS = 5
SHEEP = 15
WAIT = False


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


def configuration(parser):
    global CONFIG_FILE, SAVE_DIR, ROUNDS, SHEEP, INITPOSLIMIT, SHEEPMOVEDIST, WOLFMOVEDIST, WAIT
    args, remainder_argv = parser.parse_known_args()

    levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    if args.config:
        CONFIG_FILE += args.config + ".ini"
        if os.path.isfile(CONFIG_FILE):
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            if float(config['Terrain']['InitPosLimit']) > 0:
                INITPOSLIMIT = float(config['Terrain']['InitPosLimit'])
            else:
                raise ValueError('InitPosLimit should be greater than 0.')
            if float(config['Movement']['SheepMoveDist']) > 0:
                SHEEPMOVEDIST = float(config['Movement']['SheepMoveDist'])
            else:
                raise ValueError('SheepMoveDist should be greater than 0.')
            if float(config['Movement']['WolfMoveDist']) > 0:
                WOLFMOVEDIST = float(config['Movement']['WolfMoveDist'])
            else:
                raise ValueError('WolfMoveDist should be greater than 0.')
        else:
            raise FileNotFoundError('File does not exist')

    if args.dir:
        # todo zrobic ta czesc
        SAVE_DIR = args.dir

    # todo tutaj tez to zrobic
    # if args.log:
    #     if args.log not in levels.values():
    #         print("It is not a log level.")

    if args.rounds:
        if args.rounds > 0:
            ROUNDS = args.rounds
        else:
            raise ValueError('Value should be greater than 0.')

    if args.sheep:
        if args.sheep > 0:
            SHEEP = args.sheep
        else:
            raise ValueError('Value should be greater than 0.')

    if args.wait:
        WAIT = True
