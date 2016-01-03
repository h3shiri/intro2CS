from tkinter import *
import math
from collections import namedtuple

WIDTH_SCREEN = 700
HEIGHT_SCREEN = 700
OUT_SIZE = 0.1
NUM_TICKS = 11
TICKS_L_RATIO = 0.02
ROUNDX = 3

X, Y = 0, 1


class Graph:
    """
    An object from class Graph - 
    has only one public function:
    plot_line: plot a line to the screen
    """
    def __init__(self, top, minX=-10, minY=-10, maxX=10, maxY=10):
        """
        Init a graph
        Expects a gui object and graph limits
        """
        self.__top = top
        self.__Frame = Frame(self.__top, width=WIDTH_SCREEN+OUT_SIZE,
                             height=HEIGHT_SCREEN+OUT_SIZE, bd=1, bg='#aaa')
        self.__Frame.pack()
        self.__width_screen = WIDTH_SCREEN
        self.__height_screen = HEIGHT_SCREEN
        self.__min_x_screen = OUT_SIZE*WIDTH_SCREEN
        self.__max_x_screen = (1-OUT_SIZE)*WIDTH_SCREEN
        self.__min_y_screen = OUT_SIZE*HEIGHT_SCREEN
        self.__max_y_screen = (1-OUT_SIZE)*HEIGHT_SCREEN
        self.__width_axis = self.__max_x_screen-self.__min_x_screen
        self.__height_axis = self.__max_y_screen-self.__min_y_screen
        self.__num_ticks = NUM_TICKS
        self.__ticks_l = TICKS_L_RATIO*min(HEIGHT_SCREEN, WIDTH_SCREEN)
        self.__minX = minX
        self.__maxX = maxX
        self.__minY = minY
        self.__maxY = maxY
        self.__create_graph()

    # normalize x between two edges.    
    def __norm(self, x, min_x, max_x):
        if (min_x == max_x):
            return x
        return (x-min_x)/(max_x-min_x)

    # function from x to its  normalized value in the screen
    def __x_to_screen(self, x):
        return self.__min_x_screen + \
                  self.__norm(x, self.__minX, self.__maxX)*self.__width_axis

    # function from y to its  normalized value in the screen
    def __y_to_screen(self, y):
        return self.__max_y_screen - \
                  (self.__norm(y, self.__minY, self.__maxY)*self.__height_axis)

    # caclualte the location of the ticks in the screen
    def __ticks_vals(self, minX, maxX):
        return [minX+x*(maxX-minX)/(1+self.__num_ticks)
                for x in range(0, self.__num_ticks+2)]

    # init the canvas  and add the ticks and their text value
    def __create_graph(self):
        self.__canvas = Canvas(self.__Frame, width=WIDTH_SCREEN,
                               height=HEIGHT_SCREEN, bg='#aaa',
                               highlightbackground='black', bd=1)
        self.__canvas.pack()
        self.__canvas.create_rectangle(self.__min_x_screen,
                                       self.__max_x_screen,
                                       self.__max_y_screen,
                                       self.__min_y_screen, fill='white',
                                       width=2)

        ticks_x = self.__ticks_vals(self.__minX, self.__maxX)
        ticks_y = self.__ticks_vals(self.__minY, self.__maxY)

        for t in ticks_x:
            t_screen = self.__x_to_screen(t)
            self.__canvas.create_line(t_screen,
                                      self.__min_y_screen, t_screen,
                                      self.__min_y_screen+self.__ticks_l)
            self.__canvas.create_line(t_screen,
                                      self.__max_y_screen-self.__ticks_l,
                                      t_screen, self.__max_y_screen)
            self.__canvas.create_text(t_screen,
                                      self.__max_y_screen+self.__ticks_l,
                                      text="%.2g" % t, anchor=N)

        for t in ticks_y:
            t_screen = self.__y_to_screen(t)
            self.__canvas.create_line(self.__min_x_screen, t_screen,
                                      self.__min_x_screen+self.__ticks_l,
                                      t_screen)
            self.__canvas.create_line(self.__max_x_screen-self.__ticks_l,
                                      t_screen, self.__max_x_screen, t_screen)
            self.__canvas.create_text(self.__min_x_screen-self.__ticks_l,
                                      t_screen, text="%.2g" % t, anchor=E)

    def plot_line(self, p1, p2, c):
        """
        Add a new line to the graph object
        Doesn't plot in case one of the points is out of the graph range
        """

        line = (p1, p2)
        if self.__line_in_range(line):
            screen_X = [self.__x_to_screen(p[X]) for p in line]
            screen_Y = [self.__y_to_screen(p[Y]) for p in line]
            self.__canvas.create_line(screen_X[0], screen_Y[0], screen_X[1],
                                      screen_Y[1], fill=c, width=2)

    # return true if the line is within the graph limits
    def __line_in_range(self, line):
        for p in line:

            if p[X] > self.__maxX or p[X] < self.__minX:
                return False
            if p[Y] > self.__maxY or p[Y] < self.__minY:
                return False
        return True
