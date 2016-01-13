import tkinter as tki
from tkinter import messagebox
# Set magic numbers and constants
WAIT_TIME = 1000
BOARD_SIZE = 500
TEXTBOX_SIZE = 10
TRIANGLE = 'triangle'
CIRCLE = 'circle'
LINE = 'line'
OVAL = 'oval'
RECTANGLE = 'rectangle'
COLOR_LIST = ['blue', 'red', 'violet', 'green', 'yellow', 'black', 'orange']

HELP_MESSAGE = "To use this application:\n 1) please select a shape" \
               " and color (default is black)\n 2) select appropriate" \
               " coordinates\n"


class GuiRunner():
    """
    This class is our GUI, the user can draw variety of shapes on the canvas.
    In addtion the user can see his peers and their shapes on his board.
    """
    # Init function defines all the buttons and extra options
    def __init__(self, parent, client):
        self._debug_message = "No errors yet!"
        self.client = client
        self._active_players = []
        self._parent = parent
        self.__coordinates_list = []
        self.__color = 'black'
        self.canvas = tki.Canvas(parent, width=BOARD_SIZE, height=BOARD_SIZE,
                                 highlightbackground='blue')
        self.canvas.pack(side='right')
        self.canvas.bind("<Button-1>", self.coordinate_click)
        self.UsersBox = tki.Listbox(parent, width=TEXTBOX_SIZE,
                                    height=TEXTBOX_SIZE)
        self.UsersBox.yview()
        self.UsersBox.insert(0, "online_users:")
        group = str(self.client.group)
        self.UsersBox.insert(0, group)
        self.UsersBox.pack(side='left')
        self.UsersBox.anchor('nw')
        self.ButtonTriangle = tki.Button(parent, command=self.draw_triangle,
                                         text="Triangle")
        self.ButtonTriangle.pack(side='top')
        self.ButtonLine = tki.Button(parent, command=self.draw_line,
                                     text="Line")
        self.ButtonLine.pack(side='top')
        self.ButtonRectangle = tki.Button(parent, command=self.draw_rectangle,
                                          text="Rectangle")
        self.ButtonRectangle.pack(side='top')
        self.ButtonRectangle = tki.Button(parent, command=self.draw_circle,
                                          text="Circle")
        self.ButtonRectangle.pack(side='top')
        self.color_choice = tki.StringVar()
        self.color_choice.set("Color")
        self.color_options = tki.OptionMenu(parent, self.color_choice,
                                            'violet', 'blue', 'red', 'green',
                                            'yellow', 'black', 'orange')
        self.color_options.pack(side='top')
        self.HelpOption = tki.Button(parent,
                                     command=self.display_help_message,
                                     text='Help')
        self.HelpOption.pack()
        self.DebugButton = tki.Button(parent,
                                      command=self.debug_message,
                                      text='Debug')
        self.DebugButton.pack()
    # We use after func in order to process the changes gradually
    def queue_for_running(self, func):
        self._parent.after(WAIT_TIME, func)

    # Pre-work for drawing shapes
    def draw_line(self):
        """ This function draws line on Gui
        """
        self.__coordinates_list = []
        self.__coordinates_list.append(LINE)

    def draw_circle(self):
        """ This function draws circle on Gui
        """
        self.__coordinates_list = []
        self.__coordinates_list.append(CIRCLE)

    def draw_rectangle(self):
        """ This function draws rectangle on Gui
        """
        self.__coordinates_list = []
        self.__coordinates_list.append(RECTANGLE)

    def draw_triangle(self):
        """ This function draws triangle on Gui
        """
        self.__coordinates_list = []
        self.__coordinates_list.append(TRIANGLE)

    def coordinate_click(self, event):
        """This function is a vital generic function for the coordinate click
        Draws shapes according to coordinates
        """
        coordinates_list = self.__coordinates_list
        if self.color_choice.get() == 'Color':
            self.__color = 'black'
        else:
            self.__color = self.color_choice.get()
        color = self.__color
        if len(coordinates_list) <= 1:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)

        elif (coordinates_list[-2] == LINE and
                      type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_line(first_coordinate[0], first_coordinate[1],
                                    second_coordinate[0],
                                    second_coordinate[1], fill=color, width=2)

            self.canvas.create_text(second_coordinate[0], second_coordinate[1],
                                    text=self.client.username)
            self.__coordinates_list = []
            # Send the shape creation to the server
            self.send_shape_creation('line', first_coordinate[0],
                                     first_coordinate[1],
                                     second_coordinate[0], second_coordinate[1])
        elif (coordinates_list[-2] == CIRCLE and
                      type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_oval(first_coordinate[0],
                                    first_coordinate[1], second_coordinate[0],
                                    second_coordinate[1], fill=color, width=2)
            self.canvas.create_text(second_coordinate[0], second_coordinate[1],
                                    text=self.client.username)
            self.__coordinates_list = []
            self.send_shape_creation('oval', first_coordinate[0],
                                     first_coordinate[1], second_coordinate[0],
                                     second_coordinate[1])
        elif (coordinates_list[-2] == RECTANGLE and
                      type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_rectangle(first_coordinate[0],
                                         first_coordinate[1],
                                         second_coordinate[0],
                                         second_coordinate[1],
                                         fill=color, width=2)
            self.canvas.create_text(second_coordinate[0], second_coordinate[1],
                                    text=self.client.username)
            self.__coordinates_list = []
            self.send_shape_creation('rectangle', first_coordinate[0],
                                     first_coordinate[1],
                                     second_coordinate[0],
                                     second_coordinate[1])
        elif (len(coordinates_list) >= 3):
            if (coordinates_list[-3] == TRIANGLE and
                    (type(coordinates_list[-2]) == tuple and
                             type(coordinates_list[-1]) == tuple)):
                first_coordinate = coordinates_list[-1]
                second_coordinate = coordinates_list[-2]
                third_coordinate = (event.x, event.y)
                self.canvas.create_polygon(first_coordinate[0],
                                           first_coordinate[1],
                                           second_coordinate[0],
                                           second_coordinate[1],
                                           third_coordinate[0],
                                           third_coordinate[1],
                                           fill=color, width=2)
                self.canvas.create_text(third_coordinate[0],
                                        third_coordinate[1],
                                        text=self.client.username)
                self.__coordinates_list = []
                self.send_triangle_creation('triangle', first_coordinate[0],
                                            first_coordinate[1],
                                            second_coordinate[0],
                                            second_coordinate[1],
                                            third_coordinate[0],
                                            third_coordinate[1])
        else:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)

    def display_help_message(event):
        """ This functions displays a help message,
         when clicking on help button
        """
        messagebox.showinfo('Help', HELP_MESSAGE)


    def add_to_user_box(self):
        """This function updates the online users and shows on Gui
        """
        users = list(self.client._online_users)
        for user in users:
            if user not in self._active_players:
                self.UsersBox.insert(2, user)
                self._active_players.append(user)


    def delete_user_from_user_box(self, target):
        """  This function deletes a user that left group from user box on Gui.
        After  the leave we create a new user box to avoid the
        deletion protocol
        """
        size = self.UsersBox.size()
        for i in range(size):
            temp_line = self.UsersBox.get(i)
            if temp_line == target:
                self.UsersBox.delete(i)

    def debug_message(self):
        """This functions displays a debug message,
         when clicking on help button
        """
        messagebox.showinfo('Debug', self._debug_message)

    def create_line(self, coordinates, color, username):
        """ This function creates a line on Gui according to given color
        and user that drew the shape as username given
        """
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill=color, width=2)
        self.canvas.create_text(c2_x, c2_y, text=username)

    def create_rectangle(self, coordinates, color, username):
        """ This function creates a rectangle on Gui according to given color
        and user that drew the shape as username given
        """
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_rectangle(c1_x, c1_y, c2_x, c2_y, fill=color,
                                     width=2)
        self.canvas.create_text(c2_x, c2_y, text=username)

    def create_circle(self, coordinates, color, username):
        """ This function creates a circle on Gui according to given color
        and user that drew the shape as username given
        """
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_oval(c1_x, c1_y, c2_x, c2_y, fill=color,
                                width=2)
        self.canvas.create_text(c2_x, c2_y, text=username)

    def create_triangle(self, coordinates, color, username):
        """ This function creates a triangle on Gui according to given color
        and user that drew the shape as username given
        """
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        c3_x = int(coordinates[4])
        c3_y = int(coordinates[5])
        self.canvas.create_polygon(c1_x, c1_y, c2_x, c2_y, c3_x, c3_y,
                                   fill=color, width=2)
        self.canvas.create_text(c3_x, c3_y, text=username)

    def send_shape_creation(self, shape, x1, y1, x2, y2):
        """ This function creates a new shape upon our canvas
        and sends message to server
        """
        coordinates_text = ",".join([str(x1), str(y1), str(x2), str(y2)])
        seperator = ';'
        color = self.__color
        pre_work_out = seperator.join(['shape', shape,
                                       coordinates_text, color])
        text = str(pre_work_out + '\n')
        self.client.__send_message__(text)

    def send_triangle_creation(self, shape, x1, y1, x2, y2, x3, y3):
        """This function creates a new triangle upon our canvas,
        and sends message to server
        """
        coordinates_text = ",".join([str(x1), str(y1), str(x2), str(y2),
                                     str(x3), str(y3)])
        seperator = ';'
        color = self.__color
        Pre_work_out = seperator.join(['shape', shape,
                                       coordinates_text, color])
        text = str(Pre_work_out + '\n')
        self.client.__send_message__(text)
