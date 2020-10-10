import random


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    def move(self):
        pass

    def select_move(self):
        moves = ["east", "west", "north", "south"]
        return random.choice(moves)


class Sheep(Animal):
    def __init__(self, init_pos_limit, move_dist):
        super().__init__(move_dist)
        self.init_pos_limit: float = init_pos_limit

    def init_position(self):
        self.position[0] = random.uniform(-self.init_pos_limit, self.init_pos_limit)

    def move(self):
        selected_move = self.select_move()


class Wolf(Animal):
    def __init__(self, move_dist):
        super().__init__(move_dist)


if __name__ == '__main__':
    print(random.uniform(1, 20))
