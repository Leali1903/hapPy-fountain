import socket

###################### SOCKET ######################
# Socket, um ET-Daten vom Laptop zu empfangen

HOST = '??'  # Standard loopback interface address (localhost) (host = hostname, IP address or empty string)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)