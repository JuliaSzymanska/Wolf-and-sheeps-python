from . import Commandline, Config
from .Simulation import Simulation

if __name__ == '__main__':
    parser = Commandline.init_argparse()
    parser.parse_args()
    simulation = Simulation(Config.ROUNDS, Config.SHEEP, Config.INIT_POS_LIMIT, Config.SHEEP_MOVE_DIST,
                            Config.WOLF_MOVE_DIST)
    simulation.perform_simulation()
