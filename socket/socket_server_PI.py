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



import socket


def send_data(eye_input):
    HOST = 'localhost'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected!')
        while GUI:
            client.send(eye_input)
