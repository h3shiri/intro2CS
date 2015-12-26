from screen import Screen
from math import *
import random
import copy
import ship

SCREEN_MIN_X = Screen.SCREEN_MIN_X
SCREEN_MIN_Y = Screen.SCREEN_MIN_Y
SCREEN_MAX_X = Screen.SCREEN_MAX_X
SCREEN_MAX_Y = Screen.SCREEN_MAX_Y
RADIUS_SIZE_COEFFICIENT = 10
RADIUS_NORMALIZER = -5
TORPEDO_ACCELERATION_RATE = 2
TORPEDO_RADIUS = 4
MAX_AGE = 200

class Torpedo:

    def __init__(self, X_coordinate, Y_coordinate, x_speed, y_speed, direction):
        self.__x_coordinate = X_coordinate
        self.__y_coordinate = Y_coordinate
        self.__coordinates = (X_coordinate, Y_coordinate)
        self.__direction = radians(direction)
        self.__x_speed = x_speed + (TORPEDO_ACCELERATION_RATE * cos(radians(direction)))
        self.__y_speed = y_speed + (TORPEDO_ACCELERATION_RATE * sin(radians(direction)))
        self.radius = TORPEDO_RADIUS
        self.__age = 0


    def coordinate_X(self):
        return self.__x_coordinate

    def coordinate_Y(self):
        return self.__y_coordinate

    def heading(self):
        return self.__direction

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

    def update_age(self):
        self.__age += 1
        return (self.__age >= MAX_AGE)



