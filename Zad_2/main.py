import csv
import json
import logging
import msvcrt
from typing import Union

import Animals
import Commandline
import Config
import LoggingUtil


class Simulation:
    def __init__(self, rounds: int, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float,
                 wolf_move_dist: float):
        self.number_of_sheep: int = number_of_sheep
        self.sheep: [Animals.Sheep] = []
        self.initialize_sheep(number_of_sheep, init_pos_limit, sheep_move_dist)
        self.wolf: Animals.Wolf = Animals.Wolf(wolf_move_dist, self.sheep)
        self.dead_sheep_index: Union[int, None] = None
        self.rounds = rounds
        self.list_to_write_json_file = []
        self.list_to_write_csv_file = []
        self.round_num = 0

    @LoggingUtil.monitor_results
    def initialize_sheep(self, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float):
        logging.debug("Calling a function - initialize_sheep - that initializes sheep's. "
                      "The function takes three parameters, number of sheep: ", number_of_sheep,
                      "initialization position limit: ", init_pos_limit,
                      "sheep move distance: ", sheep_move_dist,)
        for i in range(number_of_sheep):
            self.sheep.append(Animals.Sheep(init_pos_limit, sheep_move_dist))

    @LoggingUtil.monitor_results
    def perform_simulation(self):
        logging.debug("Calling a function - perform_simulation - that performs simulation. "
                      "The function takes no parameters. ")
        living_sheep_count = self.number_of_sheep
        self.display_and_store_simulation_information(living_sheep_count)

        while self.round_num < self.rounds and living_sheep_count > 0:

            [x.move() for x in self.sheep]

            self.dead_sheep_index = self.wolf.move()

            if self.dead_sheep_index:
                living_sheep_count -= 1

            self.round_num += 1
            self.display_and_store_simulation_information(living_sheep_count)
            if Config.WAIT and (self.round_num < self.rounds and living_sheep_count > 0):
                print("Press any key to continue...")
                msvcrt.getch()

        self.save_to_json_file()
        self.save_to_csv_file()

    @LoggingUtil.monitor_results
    def display_and_store_simulation_information(self, living_sheep_count):
        logging.debug(
            "Calling a function - display_and_store_simulation_information - "
            "that calls functions to display information. "
            "The function takes one parameter, actual number of living sheep: ", living_sheep_count,)
        self.show_information()
        self.append_to_json_list()
        self.append_to_csv_list(living_sheep_count)

    @LoggingUtil.monitor_results
    def show_information(self, ):
        logging.debug("Calling a function - show_information - that shows information about simulation. "
                      "The function takes no parameters. ")
        print("Round number: ", self.round_num)
        print("Wolf position: (", round(self.wolf.position[0], 3), ", ", round(self.wolf.position[1], 3), ")")
        number_of_alive: int = 0
        for s in self.sheep:
            if s.is_alive:
                number_of_alive += 1
        print("Number of alive sheep: ", number_of_alive)
        print("Index of the eaten sheep: ", self.dead_sheep_index, "\n")

    @LoggingUtil.monitor_results
    def append_to_json_list(self):
        logging.debug("Calling a function - append_to_json_list - that adds information to list to write to json. "
                      "The function takes no parameters. ")
        sheep_position: [[int, int]] = []
        for s in self.sheep:
            if s.is_alive:
                sheep_position.append([s.position[0], s.position[1]])
            else:
                sheep_position.append(None)
        self.list_to_write_json_file.append({
            "round_no": self.round_num,
            "wolf_pos": [self.wolf.position[0], self.wolf.position[1]],
            "sheep_pos": sheep_position,
        })

    @LoggingUtil.monitor_results
    def save_to_json_file(self):
        logging.debug("Calling a function - save_to_json_file - that saves information to json file. "
                      "The function takes no parameters. ")
        json_object = json.dumps(self.list_to_write_json_file, indent=3)
        with open(Config.SAVE_DIR + 'pos.json', 'w') as json_file:
            json_file.write(json_object)

    @LoggingUtil.monitor_results
    def append_to_csv_list(self, number_of_alive_sheep: int):
        logging.debug("Calling a function - append_to_csv_list - that adds information to list to write to csv. "
                      "The function takes no parameters. ")
        self.list_to_write_csv_file.append([self.round_num, number_of_alive_sheep])

    @LoggingUtil.monitor_results
    def save_to_csv_file(self):
        logging.debug("Calling a function - save_to_csv_file - that saves information to csv file. "
                      "The function takes no parameters. ")
        with open(Config.SAVE_DIR + 'alive.csv', mode='w', newline='') as alive_file:
            csv_writer = csv.writer(alive_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)

            for round_number in range(self.rounds):
                csv_writer.writerow(self.list_to_write_csv_file[round_number])


if __name__ == '__main__':
    parser = Commandline.init_argparse()
    parser.parse_args()
    logging.warning('Test on warning')
    simulation = Simulation(Config.ROUNDS, Config.SHEEP, Config.INIT_POS_LIMIT, Config.SHEEP_MOVE_DIST,
                            Config.WOLF_MOVE_DIST)
    simulation.perform_simulation()
    logging.info('Test on info')
