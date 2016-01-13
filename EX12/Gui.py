import tkinter as tki
from tkinter import messagebox
WAIT_TIME = 1000
TRIANGLE = 'triangle'
CIRCLE = 'circle'
LINE = 'line'
RECTANGLE = 'rectangle'
COLOR_LIST = ['blue', 'red', 'violet', 'green', 'yellow', 'black', 'orange']

#TODO: edit help message
HELP_MESSAGE = 'Help Me!!'
class GuiRunner():
    def __init__(self, parent,client):
        #Building the Gui
        self._debug_message = "No errors yet!"
        self.client = client
        self._active_players = []
        self._parent = parent
        self.__coordinates_list = []
        self.__color = 'black'
        self.canvas = tki.Canvas(parent, width=500 ,height=500, highlightbackground='blue')
        self.canvas.pack(side='right')
        self.canvas.bind("<Button-1>", self.CoordinateClick)
        self.UsersBox = tki.Listbox(parent, width=10, height=10)
        self.UsersBox.yview()
        self.UsersBox.pack(side='left')
        self.UsersBox.anchor('nw')
        self.ButtonTriangle = tki.Button(parent, command=self.DrawTriangle, text="Triangle")
        self.ButtonTriangle.pack(side='top')
        self.ButtonLine = tki.Button(parent, command=self.DrawLine, text="Line")
        self.ButtonLine.pack(side='top')
        self.ButtonRectangle = tki.Button(parent,command=self.DrawRectangle, text="Rectangle")
        self.ButtonRectangle.pack(side='top')
        self.ButtonRectangle = tki.Button(parent,command=self.DrawCircle, text="Circle")
        self.ButtonRectangle.pack(side='top')
        self.color_choice = tki.StringVar()
        self.color_choice.set("Color")
        self.color_options = tki.OptionMenu(parent, self.color_choice, 'violet', 'blue', 'red', 'green', 'yellow', 'black', 'orange')
        self.color_options.pack(side='top')
        self.HelpOption = tki.Button(parent, command=self.DisplayHelpMessage, text='Help' )
        self.HelpOption.pack()
        self.DebugButton = tki.Button(parent, command=self.DebugMessage, text='Debug')
        self.DebugButton.pack()       
    
    def queue_for_running(self,func):
        self._parent.after(WAIT_TIME,func)

    #Pre-work for drawing shapes
    def DrawLine(self):
        self.__coordinates_list = []
        self.__coordinates_list.append(LINE)
    def DrawCircle(self):
        self.__coordinates_list = []
        self.__coordinates_list.append(CIRCLE)
    def DrawRectangle(self):
            self.__coordinates_list = []
            self.__coordinates_list.append(RECTANGLE)
    def DrawTriangle(self):
        self.__coordinates_list = []
        self.__coordinates_list.append(TRIANGLE)

    def CoordinateClick(self, event):
        coordinates_list = self.__coordinates_list
        if self.color_choice.get() == 'Color':
            self.__color = 'black'
        else:
            self.__color = self.color_choice.get()
        color = self.__color
        if len(coordinates_list) <= 1:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)

        elif (coordinates_list[-2] == LINE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_line(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill=color, width=2)

            self.canvas.create_text(second_coordinate[0],second_coordinate[1], text=self.client.username)
            self.__coordinates_list = []
            # Send the shape creation to the server
            self.Send_Shape_creation('line', first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1])
        elif (coordinates_list[-2] == CIRCLE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_oval(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill=color, width=2)
            self.canvas.create_text(second_coordinate[0],second_coordinate[1], text=self.client.username)
            self.__coordinates_list = []
            self.Send_Shape_creation('oval', first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1])
        elif (coordinates_list[-2] == RECTANGLE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_rectangle(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill=color, width=2)
            self.canvas.create_text(second_coordinate[0],second_coordinate[1], text=self.client.username)
            self.__coordinates_list = []
            self.Send_Shape_creation('rectangle', first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1])
        elif (len(coordinates_list) >= 3):
            if (coordinates_list[-3] == TRIANGLE and \
               (type(coordinates_list[-2]) == tuple and type(coordinates_list[-1]) == tuple)):
                first_coordinate = coordinates_list[-1]
                second_coordinate = coordinates_list[-2]
                third_coordinate = (event.x, event.y)
                self.canvas.create_polygon(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], third_coordinate[0], third_coordinate[1], fill=color, width=2)
                self.canvas.create_text(third_coordinate[0],third_coordinate[1], text=self.client.username)
                self.__coordinates_list = []
                self.Send_triangle_creation('triangle', first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], third_coordinate[0], third_coordinate[1])
        else:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)
    def DisplayHelpMessage(event):
        messagebox.showinfo('Help', HELP_MESSAGE)

    def AddToUserBox(self):
        users = list(self.client._online_users)
        for user in users:
            if user not in self._active_players:
                self.UsersBox.insert(0, user)
                self._active_players.append(user)
    #after leave we create a new user box to avoid the deletion protocol
    def deleteUserFromUserBox(self, target):
        size = self.UsersBox.size()
        for i in range(size):
            temp_line = self.UsersBox.get(i)
            if temp_line == target:
                self.UsersBox.delete(i)
        
    def DebugMessage(self):
        messagebox.showinfo('Debug', self._debug_message)

    def createLine(self, coordinates, color, username):
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill=color, width=2)
        self.canvas.create_text(c2_x,c2_y, text=username)

    def createRectangle(self, coordinates,color, username):
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_rectangle(c1_x, c1_y, c2_x, c2_y, fill=color, width=2)
        self.canvas.create_text(c2_x,c2_y, text=username)

    def createCircle(self, coordinates, color, username):
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        self.canvas.create_oval(c1_x, c1_y, c2_x, c2_y, fill=color, width=2)
        self.canvas.create_text(c2_x,c2_y, text=username)

    def createTriangle(self, coordinates, color, username):
        c1_x = int(coordinates[0])
        c1_y = int(coordinates[1])
        c2_x = int(coordinates[2])
        c2_y = int(coordinates[3])
        c3_x = int(coordinates[4])
        c3_y = int(coordinates[5])
        self.canvas.create_polygon(c1_x, c1_y, c2_x, c2_y, c3_x, c3_y, fill=color, width=2)
        self.canvas.create_text(c3_x,c3_y, text=username)

    def Send_Shape_creation(self,shape, x1, y1, x2, y2):
        coordinates_text = ",".join([str(x1), str(y1), str(x2), str(y2)])
        username = self.client.username
        seperator = ';'
        color = self.__color
        Pre_work_out = seperator.join(['shape', shape, coordinates_text,color])
        text = str(Pre_work_out+'\n')
        self.client.__send_message__(text)

    def Send_triangle_creation(self, shape, x1, y1, x2, y2, x3, y3):
        coordinates_text = ",".join([str(x1), str(y1), str(x2), str(y2), str(x3), str(y3)])
        username = self.client.username
        seperator = ';'
        color = self.__color
        Pre_work_out = seperator.join(['shape', shape, coordinates_text,color])
        text = str(Pre_work_out+'\n')
        self.client.__send_message__(text)    
