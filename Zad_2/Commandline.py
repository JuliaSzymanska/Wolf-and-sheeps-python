import argparse
import logging
import os

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
    global SAVE_DIR, ROUNDS, SHEEP, INITPOSLIMIT, SHEEPMOVEDIST, WOLFMOVEDIST, WAIT
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
            import configparser
            config = configparser.ConfigParser()
            config.read(config_file)
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

    # tworzy się katalog, ale pliki zapisuja się w domyślnej ścieżce, a katalog tworzy sie na koniec programu.
    # Natomiast jeśli katalog istnieje to działa poprawnie
    if args.dir:
        if os.path.exists(args.dir) and os.path.isdir(args.dir):
            SAVE_DIR = args.dir + '/'
        else:
            try:
                os.mkdir(args.dir)
                SAVE_DIR = args.dir + '/'
            except OSError:
                raise OSError('Creation of the directory %s failed ' % SAVE_DIR)
            else:
                raise OSError('Successfully created the directory %s ' % SAVE_DIR)

    if args.log:
        if args.log not in levels.keys():
            raise ValueError('This log level does not exist.')
        else:
            logging.basicConfig(filename=SAVE_DIR + 'chase.log',
                                filemode='w',
                                level=levels[args.log])

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
