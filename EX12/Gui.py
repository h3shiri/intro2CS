import tkinter as tki
TRIANGLE = 'triangle'
CIRCLE = 'circle'
LINE = 'line'
RECTANGLE = 'rectangle'

class GuiRunner():
    def __init__(self, parent):
        #Building the Gui
        self._parent = parent
        self.__coordinates_list = []
        self.canvas = tki.Canvas(parent, width=200 ,height=200, highlightbackground='blue')
        self.canvas.pack(side='right')
        self.canvas.bind("<Button-1>", self.CoordinateClick)
        self.TextBox = tki.Listbox(parent, width=30, height=20)
        self.TextBox.pack(side='left')
        self.TextBox.anchor('nw')
        self.scale = tki.Scale(parent, from_=0, to=200)
        self.scale.pack(side='left')
        self.ButtonTriangle = tki.Button(parent, command=self.DrawTriangle, text="Triangle")
        self.ButtonTriangle.pack(side='top')
        self.ButtonLine = tki.Button(parent, command=self.DrawLine, text="Line")
        self.ButtonLine.pack(side='top')
        self.ButtonRectangle = tki.Button(parent,command=self.DrawRectangle, text="Rectangle")
        self.ButtonRectangle.pack(side='top')
        self.ButtonRectangle = tki.Button(parent,command=self.DrawCircle, text="Circle")
        self.ButtonRectangle.pack(side='top')

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
        if len(coordinates_list) <= 1:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)

        elif (coordinates_list[-2] == LINE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_line(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill='red', width=2)
            self.__coordinates_list = []
        elif (coordinates_list[-2] == CIRCLE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_oval(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill='red', width=2)
            self.__coordinates_list = []
        elif (coordinates_list[-2] == RECTANGLE and type(coordinates_list[-1]) == tuple):
            first_coordinate = coordinates_list[-1]
            second_coordinate = (event.x, event.y)
            self.canvas.create_rectangle(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], fill='red', width=2)
            self.__coordinates_list = []
        elif (len(coordinates_list) >= 3):
            if (coordinates_list[-3] == TRIANGLE and \
               (type(coordinates_list[-2]) == tuple and type(coordinates_list[-1]) == tuple)):
                first_coordinate = coordinates_list[-1]
                second_coordinate = coordinates_list[-2]
                third_coordinate = (event.x, event.y)
                self.canvas.create_polygon(first_coordinate[0], first_coordinate[1], second_coordinate[0], second_coordinate[1], third_coordinate[0], third_coordinate[1], fill='pink', width=2)
                self.__coordinates_list = []
        else:
            coordinates = (event.x, event.y)
            self.__coordinates_list.append(coordinates)

Ultimate_root = tki.Tk()
GuiRunner(Ultimate_root)
Ultimate_root.mainloop()

