import random


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    def move(self):
        pass

    def select_move(self):
        pass


class Sheep(Animal):
    def __init__(self, init_pos_limit, move_dist):
        super().__init__(move_dist)
        self.init_pos_limit: float = init_pos_limit
        self.init_position()

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


class Wolf(Animal):
    def __init__(self, move_dist):
        super().__init__(move_dist)


if __name__ == '__main__':
    sheep = Sheep(10.0, 0.5)
    print(sheep.position)
    sheep.move()
    print(sheep.position)
