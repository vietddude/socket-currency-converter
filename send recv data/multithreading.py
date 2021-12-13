import tkinter as tk
import socket
from tkinter import *
import threading

HEADER = 64
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"



def handle_client(conn, addr):
    print(f"[NEW CONNECTION {addr} connected.\n")
    f"[NEW CONNECTION {addr} connected.\n"
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def config():
    server_running = False

    def all_point():
        nonlocal server_running
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(ADDR)

        def start():
            server.listen()
            print(f"[LISTENING] Server is listening on {SERVER}")
            try:
                while True:
                    conn, addr = server.accept()
                    thread = threading.Thread(target=handle_client, args=(conn, addr))
                    thread.daemon = True
                    thread.start()
                    print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")
            except KeyboardInterrupt:
                print('Error')
                server.close()
            finally:
                server.listen()
                print('End Session')
        start()

    def start_server():
        if not server_running:
            threading.Thread(target=all_point, daemon=True).start()

    root = Tk()
    root.geometry("320x240")

    start_sv = Button(text='Start', command=start_server)
    noti_field = Text(root, width=30, height=10)

    noti_field.pack()
    start_sv.pack()

    # play = Button(text='Pk', command=fix)
    # play.pack()
    root.mainloop()

config()