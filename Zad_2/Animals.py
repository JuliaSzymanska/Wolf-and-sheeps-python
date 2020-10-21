import logging
import math
import random
import LoggingUtil
from scipy.spatial import distance


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    def get_x_pos(self):
        return self.position[0]

    def get_y_pos(self):
        return self.position[1]

    def set_x_pos(self, x: float):
        self.position[0] = x

    def set_y_pos(self, y: float):
        self.position[1] = y


class Sheep(Animal):
    # TODO: nwm czy te __init__ tez mamy loggowac
    def __init__(self, init_pos_limit, move_dist):
        super().__init__(move_dist)
        self.init_pos_limit: float = init_pos_limit
        self.init_position()
        self.is_alive = True

    @LoggingUtil.monitor_results
    def init_position(self):
        self.position[0]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        self.position[1]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        logging.info("Initialized sheep position: [", self.position[0], ", ", self.position[1], "]")

    @LoggingUtil.monitor_results
    def move(self):

        # todo shouldn't log inner fun?
        @LoggingUtil.monitor_results
        def select_move() -> str:
            moves: [str] = ["east", "west", "north", "south"]
            choosen_move: str = random.choice(moves)
            return choosen_move

        if self.is_alive:
            selected_move: str = select_move()
            if selected_move == "east":
                self.position[0] += self.move_dist
                logging.info("Sheep moved to ", selected_move, ". New sheep position: : [", self.position[0], ", ",
                             self.position[1], "]")
                return
            elif selected_move == "west":
                self.position[0] -= self.move_dist
                logging.info("Sheep moved to ", selected_move, ". New sheep position: : [", self.position[0], ", ",
                             self.position[1], "]")
                return
            elif selected_move == "north":
                self.position[1] += self.move_dist
                logging.info("Sheep moved to ", selected_move, ". New sheep position: : [", self.position[0], ", ",
                             self.position[1], "]")
                return
            elif selected_move == "south":
                self.position[1] -= self.move_dist
                logging.info("Sheep moved to ", selected_move, ". New sheep position: : [", self.position[0], ", ",
                             self.position[1], "]")
                return

    @LoggingUtil.monitor_results
    def die(self):
        logging.info("The sheep has died. ")
        self.is_alive = False


class Wolf(Animal):
    def __init__(self, move_dist, game_sheep):
        super().__init__(move_dist)
        # todo fix (check if type is list of type?)
        if type(game_sheep[0]) is Sheep:
            self.game_sheep: [Sheep] = game_sheep

    @LoggingUtil.monitor_results
    def calculate_distance(self, one_game_sheep: Sheep):
        distance_to_sheep = distance.euclidean([self.position], [one_game_sheep.position])
        return distance_to_sheep

    @LoggingUtil.monitor_results
    def move(self):
        """
        Finds closest sheep to the wolf.
        If the sheep is closer than wolf's move distance the sheep dies.
        If it's further the wolf moves in a straight line to the closest sheep.
        :return: Did sheep die
        """
        # todo pobierać nazwę funkcji w kodzie
        #   dodać funkcję która loguje 'za nas'
        #   najlepiej dodać moduł do logowanie
        #   https://stackoverflow.com/a/10974508
        #   https://stackoverflow.com/a/54209647
        #   https://docs.python.org/3/howto/logging.html
        distance_to_sheep = -1
        sheep_index = -1

        for index, s in enumerate(self.game_sheep):
            if s.is_alive:
                current_dist = self.calculate_distance(s)
                if sheep_index == -1:
                    sheep_index = index
                    distance_to_sheep = current_dist
                if current_dist < distance_to_sheep:
                    distance_to_sheep = current_dist
                    sheep_index = index

        if distance_to_sheep < self.move_dist:
            self.game_sheep[sheep_index].die()
            return sheep_index

        x_pos_sheep = self.game_sheep[sheep_index].get_x_pos()
        y_pos_sheep = self.game_sheep[sheep_index].get_y_pos()

        # calculate coefficients for x and y pos change
        norm: float = math.sqrt((x_pos_sheep - self.get_x_pos()) ** 2 + (y_pos_sheep - self.get_y_pos()) ** 2)
        dir_x = (x_pos_sheep - self.get_x_pos()) / norm
        dir_y = (y_pos_sheep - self.get_y_pos()) / norm

        # change x and y position of the wolf
        self.set_x_pos(self.get_x_pos() + self.move_dist * dir_x)
        self.set_y_pos(self.get_y_pos() + self.move_dist * dir_y)
        return False
