import Animals
import json
import csv


class Simulation:
    def __init__(self, rounds: int, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float,
                 wolf_move_dist: float):
        self.number_of_sheep: int = number_of_sheep
        self.sheep: [Animals.Sheep] = []
        self.initialize_sheep(number_of_sheep, init_pos_limit, sheep_move_dist)
        self.wolf: Animals.Wolf = Animals.Wolf(wolf_move_dist, self.sheep)
        self.changes: [int] = []
        self.rounds = rounds
        self.list_to_write_json_file = []
        self.list_to_write_csv_file = []

    def initialize_sheep(self, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float):
        for i in range(number_of_sheep):
            self.sheep.append(Animals.Sheep(init_pos_limit, sheep_move_dist))

    def perform_simulation(self):
        round_number: int = 0
        is_sheep_alive = [True] * self.number_of_sheep
        self.show_information(round_number)
        self.save_list_to_write_to_file(round_number)
        self.save_list_to_csv_file(round_number, is_sheep_alive)
        while round_number < self.rounds and sum(is_sheep_alive) > 0:
            for one_sheep in self.sheep:
                one_sheep.move()
            self.wolf.move()
            round_number += 1
            is_sheep_alive_in_round = [True] * self.number_of_sheep
            for index_of_sheep in range(self.number_of_sheep):
                if not self.sheep[index_of_sheep].is_alive:
                    is_sheep_alive_in_round[index_of_sheep] = False
            self.changes = [i for i in range(self.number_of_sheep) if is_sheep_alive_in_round[i] != is_sheep_alive[i]]
            is_sheep_alive = is_sheep_alive_in_round
            self.show_information(round_number)
            self.save_list_to_write_to_file(round_number)
            self.save_list_to_csv_file(round_number, is_sheep_alive)
        self.save_to_json_file()
        self.save_to_csv_file()

    def show_information(self, round_number: int):
        print("Round number: ", round_number)
        print("Wolf position: (", round(self.wolf.position[0], 3), ", ", round(self.wolf.position[1], 3), ")")
        number_of_alive: int = 0
        for s in self.sheep:
            if s.is_alive:
                number_of_alive += 1
        print("Number of alive sheep: ", number_of_alive)
        print("Index of the eaten sheep: ", self.changes)
        print("")

    def save_list_to_write_to_file(self, round_number: int):
        sheep_position: [[int, int]] = []
        for s in self.sheep:
            if s.is_alive:
                sheep_position.append([s.position[0], s.position[1]])
            else:
                sheep_position.append(None)
        self.list_to_write_json_file.append({
            "round_no": round_number,
            "wolf_pos": [self.wolf.position[0], self.wolf.position[1]],
            "sheep_pos": sheep_position,
        })

    def save_to_json_file(self):
        json_object = json.dumps(self.list_to_write_json_file, indent=3)
        with open('pos.json', 'w') as json_file:
            json_file.write(json_object)

    def save_list_to_csv_file(self, round_number: int, is_sheep_alive: [bool]):
        number_of_alive_sheep: int = 0
        for i in is_sheep_alive:
            if i:
                number_of_alive_sheep += 1

        self.list_to_write_csv_file.append([round_number, number_of_alive_sheep])

    def save_to_csv_file(self):
        with open('alive.csv', mode='w') as alive_file:
            alive_writer = csv.writer(alive_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
            for round_number in range(self.rounds):
                alive_writer.writerow(self.list_to_write_csv_file[round_number])


if __name__ == '__main__':
    simulation = Simulation(50, 15, 10.0, 0.5, 1.0)
    simulation.perform_simulation()
