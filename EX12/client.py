import sys
import socket
import math
import PIL
import copy
import Gui
import tkinter as tki
import select


HOST = sys.argv[1]
PORT = int(sys.argv[2])
MAX_DATA_CHUNK = 1024
MSG_DELIMETER = b'\n'
    
class Client():
    """docstring for Client"""
    def __init__(self, username,group):
        self._online_users = set()
        self.username = username
        self._online_users.add(username)
        self.group = group
        self.connect_to_server()
        Ultimate_root = tki.Tk()
        self.gui = Gui.GuiRunner(Ultimate_root,self)
        self.gui.AddToUserBox()
        self.gui.queue_for_running(self.recieve_server_messages)
        Ultimate_root.mainloop()

    def __send_message__(self,msg):
        self.socket.sendall(msg.encode())

    def connect_to_server(self):
        self.socket = socket.socket()
        self.socket.connect((HOST,PORT))
        self.__send_message__('join;%s;%s\n'%(username,group))
    
    def recieve_server_messages(self):
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
                    #TODO: USe the message accordingly..
                    print("serverMessage:%s"%(message))
            break
        self.gui.queue_for_running(self.recieve_server_messages)

    def event_handler(self, message_class):
        action = (message_class.actions_types)[0]
        # join,leave or Users actions.
        print(message_class.actions_types)
        if action == "users":
            users = message_class._raw_list[1].split(",")
            for user in users:
                self._online_users.add(user)
                self.gui.AddToUserBox()
        
        elif action == "join":
            user = message_class._raw_list[1]
            self._online_users.add(user)
            self.gui.AddToUserBox()
        elif action == 'leave':
            user = message_class._raw_list[1]
            if user in self._online_users:
                self._online_users.remove(user)
                self.gui.deleteUserFromUserBox(user)
        elif action == "error":
            error = message_class._raw_list[1]
            self.gui._debug_message = error
        elif action == "shape":
            self.shape_proccesor(message_class)

        message_class.actions_types.remove(action)
    
    def shape_proccesor(self, message_class):
        username = message_class._raw_list[1]
        shape = message_class._raw_list[2]
        color = message_class._raw_list[-1]
        coordinates = message_class._raw_list[3].split(",")
        if shape == 'line' and message_class._raw_list[1] != self.username:
            self.gui.createLine(coordinates, color)
        elif shape == 'rectangle' and message_class._raw_list[1] != self.username:
            self.gui.createRectangle(coordinates, color)
        elif shape == 'oval' and message_class._raw_list[1] != self.username:
            self.gui.createCircle(coordinates, color)


class Message():
    """docstring for Message"""
    def __init__(self, Server_message):
        self.__server_message = Server_message
        self.actions_types = ["cookie"]
        self.decipher()

    def decipher(self):
        messages = self.__server_message.split("\n")
        for message in messages:
            if len(message) != 0:
                new_message_parameters = message.split(";")
                new_message_parameters[-1] = new_message_parameters[-1].strip("\n")
                self._raw_list = new_message_parameters
                if self.actions_types[0] == "cookie":
                    self.actions_types[0] = new_message_parameters[0]
                else:
                    self.actions_types.append(new_message_parameters[0])





if __name__ == '__main__':
    username = sys.argv[3]
    group = sys.argv[4]
    Client(username, group)
