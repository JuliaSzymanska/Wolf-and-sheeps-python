import math
import random
from scipy.spatial import distance


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    def move(self):
        pass


class Sheep(Animal):
    def __init__(self, init_pos_limit, move_dist):
        super().__init__(move_dist)
        self.init_pos_limit: float = init_pos_limit
        self.init_position()
        self.is_alive = True

    def init_position(self):
        self.position[0]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        self.position[1]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)

    def select_move(self) -> str:
        moves: [str] = ["east", "west", "north", "south"]
        return random.choice(moves)

    def move(self):
        if self.is_alive:
            selected_move: str = self.select_move()
            if selected_move == "east":
                self.position[0] += self.move_dist
                return
            elif selected_move == "west":
                self.position[0] -= self.move_dist
                return
            elif selected_move == "north":
                self.position[1] += self.move_dist
                return
            elif selected_move == "south":
                self.position[1] -= self.move_dist
                return

    def die(self):
        self.is_alive = False


class Wolf(Animal):
    def __init__(self, move_dist, game_sheep):
        super().__init__(move_dist)
        self.game_sheep: [Sheep] = game_sheep

    def calculate_distance(self, one_game_sheep: Sheep):
        return distance.euclidean([self.position], [one_game_sheep.position])
        # return math.sqrt((int(one_game_sheep.position[0] - self.position[0])) ^ 2 + (int(
        #     one_game_sheep.position[1] - self.position[1])) ^ 2)

    def move(self):
        distance_to_sheep = [[], []]
        for s in self.game_sheep:
            if s.is_alive:
                distance_to_sheep[0].append(self.calculate_distance(s))
                distance_to_sheep[1].append(self.game_sheep.index(s))

        sheep_index = distance_to_sheep[1][distance_to_sheep[0].index(min(distance_to_sheep[0]))]
        distance_index = distance_to_sheep[0].index(min(distance_to_sheep[0]))
        if distance_to_sheep[0][distance_index] < self.move_dist:
            self.game_sheep[sheep_index].die()
            return
        x_diff = self.position[0] - self.game_sheep[sheep_index].position[0]
        y_diff = self.position[1] - self.game_sheep[sheep_index].position[1]
        if math.fabs(x_diff) <= y_diff:
            if x_diff < 0:
                self.position[0] += self.move_dist
            else:
                self.position[0] -= self.move_dist
        else:
            if y_diff < 0:
                self.position[1] += self.move_dist
            else:
                self.position[1] -= self.move_dist


# Todo: trzeba jakoś przechowywać info, ktora owca w tej turze została zjedzona
def show_information(round_number: int, wolf: Wolf, sheep: [Sheep], changes: [int]):
    print("Round number: ", round_number)
    print("Wolf position: (", round(wolf.position[0], 3), ", ", round(wolf.position[1], 3), ")")
    number_of_alive: int = 0
    for s in sheep:
        if s.is_alive:
            number_of_alive += 1
    print("Number of alive sheep: ", number_of_alive)
    print("Index of the eaten sheep: ", changes)
    print("")


def perform_simulation(rounds: int, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float,
                       wolf_move_dist: float):
    sheep: [Sheep] = []
    for i in range(number_of_sheep):
        sheep.append(Sheep(init_pos_limit, sheep_move_dist))
    wolf: Wolf = Wolf(wolf_move_dist, sheep)
    i: int = 0
    changes: [int] = []
    show_information(i, wolf, sheep, changes)
    is_sheep_alive = [True] * number_of_sheep
    while i < rounds and sum(is_sheep_alive) > 0:
        for j in sheep:
            j.move()
        wolf.move()
        i += 1
        is_sheep_alive_in_round = [True] * number_of_sheep
        for k in range(len(sheep)):
            if not sheep[k].is_alive:
                is_sheep_alive_in_round[k] = False
        changes = [i for i in range(number_of_sheep) if is_sheep_alive_in_round[i] != is_sheep_alive[i]]
        is_sheep_alive = is_sheep_alive_in_round
        show_information(i, wolf, sheep, changes)


if __name__ == '__main__':
    perform_simulation(50, 15, 10.0, 0.5, 1.0)
