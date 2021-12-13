import socket
import threading
import json

HEADER = 64
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

LOGIN = 'login'
ACCOUNT_DATABASE = 'data.json'

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     listAccount = []
#     connected = True
#     while connected:
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False
#             if msg == LOGIN:
#                 listAccount.append(msg)
#                 listAccount.append(msg)
#                 conn.send("Login data received".encode(FORMAT))
#             print(listAccount)
#             print(f"[{addr}] {msg}")
#
#             conn.send("Msg received".encode(FORMAT))
#
#     conn.close()


# def clientLogin(conn):
#     user_length = conn.recv(HEADER).decode(FORMAT)
#     user = conn.recv(user_length).decode(FORMAT)
#     passwd_length = conn.recv(HEADER).decode(FORMAT)
#     passwd = conn.recv(passwd_length).decode(FORMAT)
#     user_data = {user: passwd}

def clientSignup(conn):
    user_length = conn.recv(HEADER).decode(FORMAT)
    user = conn.recv(user_length).decode(FORMAT)
    passwd_length = conn.recv(HEADER).decode(FORMAT)
    passwd = conn.recv(passwd_length).decode(FORMAT)
    user_data = {user: passwd}


def handle_client(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == LOGIN:
                clientLogin(conn)

def start():
    server.listen()
    try:
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print('Error')
        server.close()
    finally:
        print('End')
        server.close()


print("[STARTING] server is starting...")
start()