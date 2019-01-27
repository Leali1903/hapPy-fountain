import socket

###################### SOCKET ######################
# Socket, um ET-Daten vom Laptop zu senden

# HOST = 'localhost'  # Standard loopback interface address (localhost) (host = hostname, IP address or empty string)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     print('Connecting...')
#     s.connect((HOST, PORT))
#
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)

# import socket
#
#
# def send_data(eye_input):
#     HOST = '172.16.104.168'
#     PORT = 65432
#
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#         client.connect((HOST, PORT))
#         print('Connected!')
#         client.send(eye_input)
#
#
# send_data('Hallo')

import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()


