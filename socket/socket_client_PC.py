# import socket
#
#
# # Socket zum Empfang von ET Daten vom PC
# HOST = ''  # Linas IP address
# PORT = 65432        # The port used by the server
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall('et_input.json')
#     data = s.recv(65432)
#
# print('Received', repr(data))


# import socket
#
#
# def receive_data():
#     HOST = "0.0.0.0"
#     PORT = 65432
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#
#         server.bind(('', PORT))
#         server.listen(1) # soll nur eine Verbindung eingehen
#         while True:
#             connection, address = server.accept()
#             connection.setblocking(False)
#             eye_input = connection.recv(64)
#             self.accept_socket.recv(buffer_size)
#             if len(buf) > 0:
#                 print(eye_input)
#                 break
#
#
# receive_data()

# import socket
#
#
# def client_program():
#     host = socket.gethostname()  # as both code is running on same pc
#     port = 5000  # socket server port number
#
#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server
#
#     message = input(" -> ")  # take input
#
#     while message.lower().strip() != 'bye':
#         client_socket.send(message.encode())  # send message
#         data = client_socket.recv(1024).decode()  # receive response
#
#         print('Received from server: ' + data)  # show in terminal
#
#         message = input(" -> ")  # again take input
#
#     client_socket.close()  # close the connection
#
#
# if __name__ == '__main__':
#     client_program()

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))