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


import socket


def receive_data():
    HOST = 'localhost'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1) # soll nur eine Verbindung eingehen
        while True:
            connection, address = server.accept()
            eye_input = connection.recv(64)
            if len(buf) > 0:
                print eye_input
                break