import math
import copy
import random
import screen


SCREEN_MIN_X = screen.Screen.SCREEN_MIN_X
SCREEN_MIN_Y = screen.Screen.SCREEN_MIN_Y
SCREEN_MAX_X = screen.Screen.SCREEN_MAX_X
SCREEN_MAX_Y = screen.Screen.SCREEN_MAX_Y
SHIP_RADIUS = 1

# Define the ship class see extra documentation inside
class Ship:

    # Initialise using given location
    def __init__(self):

        X_coordinate = random.randint(SCREEN_MIN_X, SCREEN_MAX_X)
        Y_coordinate = random.randint(SCREEN_MIN_Y, SCREEN_MAX_Y)
        self.__x_coordinate = X_coordinate
        self.__y_coordinate = Y_coordinate
        self.__coordinates = (X_coordinate, Y_coordinate)
        self.__direction = 0
        self.__x_speed = 0
        self.__y_speed = 0
        self.__speed = 0
        self.radius = SHIP_RADIUS
        self.life = 3

    def X_speed(self):
        return self.__x_speed
    def Y_speed(self):
        return self.__y_speed
    # Access to coordinates from other classes
    def coordinate_X(self):
        return self.__x_coordinate
    def coordinate_Y(self):
        return self.__y_coordinate
    # In radians
    def heading(self):
        return self.__direction

    def move(self):
        delta_X = SCREEN_MAX_X - SCREEN_MIN_X
        delta_Y = SCREEN_MAX_Y - SCREEN_MIN_Y
        OldCord_X = self.__x_coordinate
        OldCord_Y = self.__y_coordinate
        NewCord_X = ((self.__x_speed + OldCord_X - SCREEN_MIN_X) % delta_X) + SCREEN_MIN_X
        NewCord_Y = ((self.__y_speed + OldCord_Y - SCREEN_MIN_Y) % delta_Y) + SCREEN_MIN_Y
        self.__x_coordinate = NewCord_X
        self.__y_coordinate = NewCord_Y

    def spin_left(self):
        SPIN_LEFT = 7
        self.__direction += SPIN_LEFT

    def spin_right(self):
        SPIN_RIGHT = -7
        self.__direction += SPIN_RIGHT

    def accelerate(self):
        CurrentDirection = math.radians(copy.deepcopy(self.__direction))
        NewSpeedX = self.__x_speed + math.cos(CurrentDirection)
        NewSpeedY = self.__y_speed + math.sin(CurrentDirection)
        self.__x_speed = NewSpeedX
        self.__y_speed = NewSpeedY










