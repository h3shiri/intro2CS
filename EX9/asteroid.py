from screen import Screen
from math import *
import random
import copy

SCREEN_MIN_X = Screen.SCREEN_MIN_X
SCREEN_MIN_Y = Screen.SCREEN_MIN_Y
SCREEN_MAX_X = Screen.SCREEN_MAX_X
SCREEN_MAX_Y = Screen.SCREEN_MAX_Y
RADIUS_SIZE_COEFFICIENT = 10
RADIUS_NORMALIZER = -5
MINIMAL_SPEED = 1
MAXIMUM_SPEED = 2
class Asteroid:

    def __init__(self, size=3, x_cord=-1, y_cord=-1, x_speed=-1, y_speed=-1):
        self.init_ast(size, x_cord, y_cord, x_speed, y_speed)

    def init_ast(self,  size, x_cord, y_cord, x_speed, y_speed):
        # if getting -1 then randomize the value, else take value gotten
        if x_cord == -1:
            self.__x_coordinate = random.randint(SCREEN_MIN_X, SCREEN_MAX_X)
        else:
            self.__x_coordinate = x_cord
        if y_cord == -1:
            self.__y_coordinate = random.randint(SCREEN_MIN_X, SCREEN_MAX_X)
        else:
            self.__y_coordinate = y_cord
        if x_speed == -1:
            self.__x_speed = random.randint(MINIMAL_SPEED, MAXIMUM_SPEED)
        else:
            self.__x_speed = x_speed
        if y_speed == -1:
            self.__y_speed = random.randint(MINIMAL_SPEED, MAXIMUM_SPEED)
        else:
            self.__y_speed = y_speed

        self.__size = size
        self.__direction = 0
        self.__speed = 0
        self.radius = ((self.__size * RADIUS_SIZE_COEFFICIENT) + RADIUS_NORMALIZER)

    def size(self):
        return self.__size

    def coordinate_X(self):
        return self.__x_coordinate

    def coordinate_Y(self):
        return self.__y_coordinate
    def speed_X(self):
        return self.__x_speed
    def speed_Y(self):
        return self.__y_speed

    def move(self):
        delta_X = SCREEN_MAX_X - SCREEN_MIN_X
        delta_Y = SCREEN_MAX_Y - SCREEN_MIN_Y
        OldCord_X = self.__x_coordinate
        OldCord_Y = self.__y_coordinate
        NewCord_X = ((self.__x_speed + OldCord_X - SCREEN_MIN_X) % delta_X) + SCREEN_MIN_X
        NewCord_Y = ((self.__y_speed + OldCord_Y - SCREEN_MIN_Y) % delta_Y) + SCREEN_MIN_Y
        self.__x_coordinate = NewCord_X
        self.__y_coordinate = NewCord_Y

    # Important collision function
    def get_intersection(self, obj):

        r1 = obj.coordinate_X() - self.coordinate_X()
        r2 = obj.coordinate_Y() - self.coordinate_Y()
        distance = sqrt(pow(r1, 2) + pow(r2, 2))

        res = (distance <= (self.radius + obj.radius))
        return res

    def get_score_for_hit(self):
        SCORE_FOR_SMALL_AST = 100
        SCORE_FOR_MEDIUM_AST = 50
        SCORE_FOR_BIG_AST = 20
        BIG = 3
        MEDIUM = 2
        SMALL = 1
        if self.__size == BIG:
            return SCORE_FOR_BIG_AST
        elif self.__size == MEDIUM:
            return SCORE_FOR_MEDIUM_AST
        elif self.__size == SMALL:
            return SCORE_FOR_SMALL_AST
        else:
            return 0
