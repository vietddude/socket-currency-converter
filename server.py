import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox

# constant values

HEADER = 64
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
NOTI_MESSAGE = []


class Server(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('435x410+400+200')
        self.resizable(width=False, height=False)
        # self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ServerUI()

    def ServerUI(self):
        self.connectFrame()
        self.serverStatusFrame()

    def connectFrame(self):
        def auto_addr():
            ip_entry.insert(0, SERVER)
            port_entry.insert(0, str(PORT))
            ip_entry.config(state='disabled')
            port_entry.config(state='disabled')

        # creating labels and entries
        connect_lf = tk.LabelFrame(self, text='Connect')
        ip_label = tk.Label(connect_lf, text='IP Address', )
        ip_entry = tk.Entry(connect_lf, textvariable=self.ip)
        port_label = tk.Label(connect_lf, text='Port')
        port_entry = tk.Entry(connect_lf, textvariable=self.port)
        auto_cb = tk.Checkbutton(connect_lf, text='Automatic')
        auto_cb.select()
        auto_cb.config(state='disabled')
        run_bt = tk.Button(connect_lf, text='Start', width=10,
                           command=lambda option=1: serverRunning(option, self.server, run_bt))
        # pack all
        ip_label.grid(row=0, column=0, padx=(20, 5), pady=(5, 0))
        ip_entry.grid(row=0, column=1, pady=(5, 0))
        port_label.grid(row=0, column=2, padx=(20, 5), pady=(5, 0))
        port_entry.grid(row=0, column=3, pady=(5, 0))
        auto_cb.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        run_bt.grid(row=1, column=3, padx=(20, 5), pady=(5, 0))
        # show frame
        connect_lf.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)
        auto_addr()

    def serverStatusFrame(self):

        def updateServerStatus():
            serverStatus_text.delete(0, tk.END)
            serverStatus_text.insert()

        server_lf = tk.LabelFrame(self, text='Server status')
        serverStatus_text = tk.Listbox(server_lf, width=40, height=15)
        scroll = tk.Scrollbar(server_lf, orient='vertical', command=serverStatus_text.yview)
        scroll.grid(row=0, column=1, sticky='ns')

        serverStatus_text.grid(row=0, column=0, padx=1, pady=3)
        server_lf.grid(row=1, column=0, padx=10, pady=10)



def serverRunning(option, server, btn):
    server_running = False

    def start_thread():
        nonlocal server_running
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("[STARTING] server is starting...")
        server.bind(ADDR)
        print(f'Server address has been bound {ADDR}')

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
            threading.Thread(target=start_thread, daemon=True).start()

    def choose_option():
        if option == 1:
            start_server()
            btn.config(state='disabled')
        elif option == 2:
            btn.config(state='normal')
            print('stop server')
        else:
            print('restart server')

    # button function
    choose_option()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION {addr} connected.\n")

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


if __name__ == "__main__":
    app = Server()
    app.mainloop()
