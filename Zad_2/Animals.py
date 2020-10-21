import logging
import math
import random
from scipy.spatial import distance


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    # todo: nwm czy w tym szkielecie tez
    def move(self):
        pass

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

    def init_position(self):
        logging.debug("Calling a function - init_position - that initializes sheep's position - x and y. "
                      "The function takes no parameters. "
                      "The function does not return anything. ")
        self.position[0]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        self.position[1]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        logging.info("Initialized sheep position: [", self.position[0], ", ", self.position[1], "]")

    def move(self):
        logging.debug("Calling a function - move - that changes sheep's position. "
                      "The function takes no parameters. "
                      "The function does not return anything. ")

        def select_move() -> str:
            moves: [str] = ["east", "west", "north", "south"]
            choosen_move: str = random.choice(moves)
            logging.debug("Calling a function - select_move - that draws the direction of sheep's movement. "
                          "The function takes no parameters. "
                          "The function returns direction: ", choosen_move)
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

    def die(self):
        logging.debug("Calling a function - die - that makes a sheep die. "
                      "The function takes no parameters. "
                      "The function does not return anything. ")
        logging.info("The sheep has died. ")
        self.is_alive = False


class Wolf(Animal):
    def __init__(self, move_dist, game_sheep):
        super().__init__(move_dist)
        # todo fix (check if type is list of type?)
        if type(game_sheep[0]) is Sheep:
            self.game_sheep: [Sheep] = game_sheep

    def calculate_distance(self, one_game_sheep: Sheep):
        distance_to_sheep = distance.euclidean([self.position], [one_game_sheep.position])
        logging.debug("Calling a function - calculate_distance - that calculates wolf's distance to sheep. "
                      "The function takes one parameter: one_game_sheep - sheep position: ", one_game_sheep,
                      "The function returns wolf's distance to sheep: ", distance_to_sheep)
        return distance_to_sheep

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
        logging.debug("Calling a function - move - that changes wolf's position. "
                      "The function takes no parameters. ")
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
            logging.debug("The function returns eaten sheep index: ", sheep_index)
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
        logging.debug("The function returns: False, because wolf have not eaten any sheep. ")
        return False
