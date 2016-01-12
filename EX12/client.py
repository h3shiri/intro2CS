import sys
import socket
import math
import PIL
import copy
import Gui
import tkinter as tki

HOST = sys.argv[1]
PORT = int(sys.argv[2])
MAX_DATA_CHUNK = 1024
    
class Client():
    """docstring for Client"""
    def __init__(self, username,group):
        self.username = username
        self.group = group
        print("Before the sockets")
        self.connect_to_server()
        Ultimate_root = tki.Tk()
        self.gui = Gui.GuiRunner(Ultimate_root,self)
        self.gui.queue_for_running(self.recieve_server_messages)
        Ultimate_root.mainloop()

    def __send_message__(self,msg):
        self.socket.sendall(msg.encode())

    def connect_to_server(self):
        self.socket = socket.socket()
        self.socket.connect((HOST,PORT))
        self.__send_message__('join;%s;%s\n'%(username,group))
    
    def recieve_server_messages(self):
        print("read messages")
        res = self.socket.recv(MAX_DATA_CHUNK)
        if res == None:
            return
        print('abcd')
        messages = res.decode()
        print(messages)
        self.gui.queue_for_running(self.recieve_server_messages)

if __name__ == '__main__':
    username = sys.argv[3]
    group = sys.argv[4]
    Client(username,group)
