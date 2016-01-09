import socket
import math
import PIL
import copy

# Receiving data from server...etc
HOST = socket.gethostname()
PORT = 6789
MAXIMUM_NUMBER_OF_QUEUED_CONNECTIONS = 0
MAX_DATA_CHUNK = 1024

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(MAXIMUM_NUMBER_OF_QUEUED_CONNECTIONS)

(transmission_socket, client_address) = server_socket.accept()

while True:
    encoded_data = transmission_socket.recv(MAX_DATA_CHUNK)
    if not encoded_data:
        # Data transmission ended
        break
    else:
        # Do something with the data
        print(encoded_data.decode('ascii'))
        reply_msg = bytes('Bye', 'ascii')
        transmission_socket.sendall(reply_msg)

transmission_socket.close()
server_socket.close()