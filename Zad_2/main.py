import math
import random


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
        return math.sqrt(int(one_game_sheep.position[0] - self.position[0]) ^ 2 + int(
            one_game_sheep.position[1] - self.position[1]) ^ 2)

    def move(self):
        distance = []
        for s in self.game_sheep:
            if s.is_alive:
                distance.append(self.calculate_distance(s))
            else:
                distance.append(None)

        index = distance.index(min(distance))
        if distance[index] < self.move_dist:
            self.game_sheep[index].die()
            return
        x_diff = self.position[0] - self.game_sheep[index].position[0]
        y_diff = self.position[1] - self.game_sheep[index].position[1]
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

def perform_simulation(rounds: int, number_of_sheep: int, init_pos_limit: float, sheep_move_dist: float, wolf_move_dist: float):
    sheep: [Sheep] = []
    for i in range(number_of_sheep):
        sheep.append([Sheep(init_pos_limit, sheep_move_dist)])
    wolf: Wolf = Wolf(wolf_move_dist, sheep)
    for i in range(rounds):



if __name__ == '__main__':
    perform_simulation(50, 15, 10.0, 0.5, 1.0)
