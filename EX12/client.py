import sys
import socket
import Gui
import tkinter as tki
import select


HOST = sys.argv[1]
PORT = int(sys.argv[2])
MAX_DATA_CHUNK = 1024
MSG_DELIMETER = b'\n'
    
class Client():
    """
    This class represents the client interface to the server,
    we also handle the server messages from her and connect to the gui.
    """
    # Initialise the class and set all basic parameters
    def __init__(self, username, group):
        self._online_users = set()
        self.username = username
        self._online_users.add(username)
        self.group = group
        self.connect_to_server()
        Ultimate_root = tki.Tk()
        self.gui = Gui.GuiRunner(Ultimate_root,self)
        self.gui.add_to_user_box()
        self.gui.queue_for_running(self.recieve_server_messages)
        Ultimate_root.mainloop()

    def __send_message__(self,msg):
        self.socket.sendall(msg.encode())

    def connect_to_server(self):
        """ this function makes socket connect to server
        """
        self.socket = socket.socket()
        self.socket.connect((HOST,PORT))
        self.__send_message__('join;%s;%s\n'%(username,group))
    
    def recieve_server_messages(self):
        """ this functions receives a message from server.
        It decodes it according to server protocol message,
        It sends the message to Gui.
        """
        while True:
            socket = self.socket
            read_list,w,x = select.select([socket], [], [], 0.01)
            for sock in read_list:
                if sock == socket:
                    data = sock.recv(MAX_DATA_CHUNK)
                    # do something with the data.
                    message = data.decode()
                    self._message_handler = Message(message)
                    self.event_handler(self._message_handler)
            break
        self.gui.queue_for_running(self.recieve_server_messages)

    def event_handler(self, message_class):
        """ This function gets a message and makes an output according to
        given information

        """
        while((len(message_class._data_list) > 0) and
                  (len(message_class.actions_types)>0)):
            action = (message_class.actions_types.pop(0))
            data = (message_class._data_list.pop(0))
            # join,leave or Users actions.
            if action == "users":
                users = data[1].split(",")
                for user in users:
                    self._online_users.add(user)
                    self.gui.add_to_user_box()
            
            elif action == "join":
                user = data[1]
                self._online_users.add(user)
                self.gui.add_to_user_box()
            elif action == 'leave':
                user = data[1]
                if user in self._online_users:
                    self._online_users.remove(user)
                    self.gui.delete_user_from_user_box(user)
            elif action == "error":
                error = data[1]
                self.gui._debug_message = error
            elif action == "shape":
                self.shape_proccesor(data)
    
    def shape_proccesor(self, data):
        """ This function gets data and makes Gui draw given information.
        Delivers username as well.
        """
        username = data[1]
        shape = data[2]
        color = data[-1]
        coordinates = data[3].split(",")
        if shape == 'line' and data[1] != self.username:
            self.gui.create_line(coordinates, color, username)
        elif shape == 'rectangle' and data[1] != self.username:
            self.gui.create_rectangle(coordinates, color, username)
        elif shape == 'oval' and data[1] != self.username:
            self.gui.create_circle(coordinates, color, username)
        elif shape == 'triangle' and data[1] != self.username:
            self.gui.create_triangle(coordinates, color, username)


class Message():
    """This class delivers messages and receives messages from server
    according to format
    Make sure that client serener are communicating"""
    #Initialise the class and set all basic parameters
    def __init__(self, Server_message):
        self.__server_message = Server_message
        self.actions_types = ["cookie"]
        self._data_list = ["Monster"]
        self.decipher()

    def decipher(self):
        """ reformats server message to useful parameters inside the class

        """
        messages = self.__server_message.split("\n")
        num_of_messages = len(messages)
        for message in messages:
            if len(message) != 0:
                new_message_parameters = message.split(";")
                new_message_parameters[-1] = \
                    new_message_parameters[-1].strip("\n")
                if self.actions_types[0] == "cookie":
                    self.actions_types[0] = new_message_parameters[0]
                    self._data_list[0] = new_message_parameters
                else:
                    self.actions_types.append(new_message_parameters[0])
                    self._data_list.append(new_message_parameters)



if __name__ == '__main__':
    username = sys.argv[3]
    group = sys.argv[4]
    Client(username, group)

