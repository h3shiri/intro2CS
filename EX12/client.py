import sys
import socket
import math
import PIL
import copy

class Message:
	def __init__(self):
		self.__send_message = ""


# Receiving data from server...etc
HOST = socket.gethostname()
PORT = 5679
MAXIMUM_NUMBER_OF_QUEUED_CONNECTIONS = 0
MAX_DATA_CHUNK = 1024
print("Before the sockets")
server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(MAXIMUM_NUMBER_OF_QUEUED_CONNECTIONS)

(transmission_socket, client_address) = server_socket.accept()
print("pre-transmition")
while True:
    encoded_data = transmission_socket.recv(MAX_DATA_CHUNK)
    if not encoded_data:
        # Data transmission ended
        print("Hello!")
        break
    else:
        # Do something with the data
        print(encoded_data.decode('ascii'))
        reply_msg = bytes('Bye', 'ascii')
        transmission_socket.sendall(reply_msg)

transmission_socket.close()
server_socket.close()
