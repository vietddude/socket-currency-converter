import socket
import tkinter as tk
from tkinter import messagebox

# constant values
HEADER = 64
PORT = 6969
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.15"
ADDR = (SERVER, PORT)

# constant color
GRAY = '#C0C0C0'


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


# def login():
#     username = input("Username: ")
#     password = input("Password: ")
#     send(username)
#     send(password)
#
#
# # GUI
# class ClientGUI(tk.Tk):
#     def __init__(self, message):
#         tk.Tk.__init__(self)
#
#         self.geometry("500x250")
#         self.title("Client")
#         self.protocol("WM_DELETE_WINDOW", self.on_closing)
#         self.resizable(width=False, height=False)
#
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=1)
#
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#
#         tk.Label(self, text=message).pack()
#         button1 = tk.Button(self, text="Connect")
#         button1.pack()
#
#     def on_closing(self):
#         if messagebox.askokcancel("Quit", "Do you want to quit?"):
#             self.destroy()
#

# class ConnectGUI(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.geometry("250x200+500+250")
#         self.resizable(width=False, height=False)
#
#         self.addr_var = tk.StringVar()
#         self.port_var = tk.StringVar()
#         cb = tk.IntVar()
#         message = tk.StringVar()
#
#         def activateCheck():
#             if cb.get() == 1:
#                 addr_entry.delete(0, 'end')
#                 port_entry.delete(0, 'end')
#                 addr_entry.insert(0, str(SERVER))
#                 port_entry.insert(0, str(PORT))
#                 addr_entry.config(state="disabled")
#                 port_entry.config(state="disabled")
#             elif cb.get() == 0:
#                 addr_entry.config(state="normal")
#                 port_entry.config(state="normal")
#                 addr_entry.delete(0, 'end')
#                 port_entry.delete(0, 'end')
#
#         self.config(bg=GRAY)
#         container = tk.Frame(self, relief='solid', bg=GRAY, padx=10, pady=10)
#
#         # creating label and entry for server address
#         addr_label = tk.Label(container, text="IP address:", bg=GRAY, )
#         addr_entry = tk.Entry(container, textvariable=self.addr_var)
#         # creating label and entry for port address
#         port_label = tk.Label(container, text="Port:", bg=GRAY)
#         port_entry = tk.Entry(container, textvariable=self.port_var)
#         # creating label for connect status
#         status = tk.Label(container, textvariable=message, bg=GRAY)
#         # creating a button to call connect function
#         sub_btn = tk.Button(container, text="CONNECT", bd=1, relief='solid', cursor='hand2', command=self.connect)
#         auto_check = tk.Checkbutton(container, text="Automatic", bg=GRAY, variable=cb,
#                                     onvalue=1, offvalue=0, command=activateCheck)
#         noti_banner = tk.Label(self, text='Please enter detail below', bg='#00a2ed', fg='white')
#
#         # placing the label and entry
#         noti_banner.pack(fill=tk.X)
#         addr_label.pack()
#         addr_entry.pack()
#         port_label.pack()
#         port_entry.pack()
#         auto_check.pack(pady=5)
#         sub_btn.pack(pady=5, ipadx=15)
#         status.pack()
#
#         container.pack(ipadx=20, ipady=5)
#
#     def connect(self):
#         if messagebox.showinfo('information', 'Connected successfully!'):
#             addr = [self.addr_var, self.port_var]
#             client.connect(addr)


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send("Hello World!")
    input()
    send("Hello World!")
    input()
    send("Hello World!")
    # send(DISCONNECT_MESSAGE)
