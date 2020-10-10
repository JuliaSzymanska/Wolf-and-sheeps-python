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


class Wolf(Animal):
    def __init__(self, move_dist):
        super().__init__(move_dist)


if __name__ == '__main__':
    print("Hi")
    a: float = 3
