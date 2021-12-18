""" All currencies' data belong to ExchangeRate-API and
European Central Bank"""

# project socket "Mang may tinh"
# 20120401 - Nguyen Duc Viet
# 20CT3

import os
import json
import sqlite3
import threading
import socket
import requests
import tkinter as tk
from datetime import date
from tkinter import messagebox

# constant values
url = 'https://open.er-api.com/v6/latest/EUR'
his_url = 'https://v6.exchangerate-api.com/v6/028bda2cc9c2abae7afcc932/history/EUR/'
HEADER = 64
PORT = 6969
LOOPBACK_SERVER = '127.0.0.1'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (LOOPBACK_SERVER, PORT)
FORMAT = 'utf-8'
DATE_FORMAT = "%#m/%#d/%Y"
DISCONNECT_MESSAGE = "DISCONNECT"
LOGIN = 'login'
SIGNUP = 'signup'
CONVERT = 'converter'
SUCCESS = 'Successful'
WRONG_PASS = 'Wrong password'
USER_ERROR = 'Username does not exist'
USER_TAKEN = 'Username has already taken'

# color constants
BG_COLOR = 'ghostwhite'
LIGHT_BLUE = '#4BB4DE'
MID_BLUE = '#3B8AC4'
DARK_BLUE = '#345DA7'


class Server(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('640x410+400+200')
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # ip address and port
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.controlFrame()

    def on_closing(self):
        if messagebox.askokcancel('Quit', 'Are you want to quit?'):
            self.destroy()

    def controlFrame(self):
        cb = tk.IntVar()

        def auto():
            if cb.get() == 1:
                ip_entry.delete(0, 'end')
                port_entry.delete(0, 'end')
                ip_entry.insert(0, '127.0.0.1')
                port_entry.insert(0, str(PORT))
                ip_entry.config(state='disabled')
                port_entry.config(state='disabled')
            elif cb.get() == 0:
                ip_entry.config(state="normal")
                port_entry.config(state="normal")
                ip_entry.delete(0, 'end')
                port_entry.delete(0, 'end')

        def fill_blank():
            if self.ip.get() == '' or self.port.get() == '':
                noti_label.config(text='Invalid input')
            else:
                config(self.ip.get(), self.port.get(), status_field)
                noti_label.config(text='')
                start_bt.config(state=tk.DISABLED)

        # icon
        self.title('Currency Converter: Server')
        logo = tk.PhotoImage(file='logo.png')
        self.iconphoto(False, logo)
        self.configure(bg=BG_COLOR)

        lb = tk.LabelFrame(self, text='Connect', bg=BG_COLOR, foreground=DARK_BLUE)
        ip_label = tk.Label(lb, text='IP Address', bg=BG_COLOR)
        ip_entry = tk.Entry(lb, textvariable=self.ip, highlightthickness=2,
                            highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        port_label = tk.Label(lb, text='Port', bg=BG_COLOR)
        port_entry = tk.Entry(lb, textvariable=self.port, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        noti_label = tk.Label(lb, text='', bg=BG_COLOR, fg='firebrick1')
        status_lf = tk.LabelFrame(self, text='Server status', foreground=DARK_BLUE, bg=BG_COLOR, bd=0)

        # where update status about server
        status_field = tk.Text(status_lf, font=('Consolas', 11), wrap=tk.WORD, width=50, height=20,
                               relief=tk.GROOVE, bd=2, state=tk.DISABLED)
        # button and check button
        auto_cb = tk.Checkbutton(lb, text='Automatic', variable=cb, onvalue=1, offvalue=0, command=auto,
                                 activebackground=BG_COLOR, bg=BG_COLOR)
        start_bt = tk.Button(lb, text='Start', width=17, command=fill_blank, bg=MID_BLUE, fg='white', borderwidth=2,
                             activebackground=BG_COLOR, activeforeground=MID_BLUE, disabledforeground=MID_BLUE)

        # pack all widgets
        ip_label.pack(anchor='w', padx=15, pady=(10, 0))
        ip_entry.pack(ipadx=15, padx=15)
        port_label.pack(anchor='w', padx=15, pady=(10, 0))
        port_entry.pack(ipadx=15, padx=15)
        auto_cb.pack(anchor='w', padx=15)
        noti_label.pack(pady=(15, 0))
        start_bt.pack(ipadx=15, pady=(0, 15))

        status_field.pack()
        status_lf.grid(row=0, column=1, padx=10, pady=10)
        lb.grid(row=0, column=0, padx=10, pady=10)


class CurrencyConverter:
    def __init__(self, conn, text_field):
        self.conn = conn
        self.status = text_field

    def convertHandle(self):

        def convert(database, date_rec, from_curr, to_curr, from_amount, rd):
            if from_curr != 'EUR':
                from_amount = from_amount / float(database[date_rec][from_curr])
            to_amount = round(from_amount * float(database[date_rec][to_curr]), rd)
            return to_amount

        def dataUpdate(date_r):
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                if getDate() not in data.keys():
                    data[getDate()] = getDataURL(url)
                if date_r not in data.keys():
                    split_date = date_r.split('/')
                    new_his_url = his_url+split_date[2]+'/'+split_date[0]+'/'+split_date[1]
                    data[date_r] = getDataURL(new_his_url)
            with open('new_data.json', 'w') as file_output:
                json.dump(data, file_output, indent=4)
            os.remove('data.json')
            os.rename('new_data.json', 'data.json')
            return data

        # get data to convert
        date_recv = getData(self.conn)
        self.conn.send('date received'.encode(FORMAT))
        from_currency = getData(self.conn)
        self.conn.send('from currency received'.encode(FORMAT))
        to_currency = getData(self.conn)
        self.conn.send('to currency received'.encode(FORMAT))
        amount = float(getData(self.conn))
        self.conn.send('amount data received'.encode(FORMAT))
        print('Data received!')

        currency_data = dataUpdate(date_recv)
        # convert and send data converted
        updateStatus(self.status, f'[CONVERT] {date_recv} from {from_currency} to {to_currency} amount {amount}')
        converted_amount = convert(currency_data, date_recv, from_currency, to_currency, amount, 4)
        self.conn.send(str(converted_amount).encode(FORMAT))
        converted_base = convert(currency_data, date_recv, from_currency, to_currency, 1, 6)
        self.conn.send(str(converted_base).encode(FORMAT))


def getDataURL(url_data):
    currencies = ["USD", "EUR", "JPY", "AUD", "CAD", "CNY", "HKD",
                  "NZD", "KRW", "SGD", "INR", "RUB", "THB", "VND"]
    new_rates = {}
    data = requests.get(url_data).json()['rates']
    for key, value in data.items():
        if key in currencies:
            new_rates[key] = value
    return new_rates


def checkLogin(conn, check_username, check_passwd, address, text_field):
    # open database
    data = sqlite3.connect('accounts.db')
    cursor = data.execute('SELECT * from ACCOUNTS where USERNAME="%s"' % check_username)
    if cursor.fetchone():
        if data.execute('SELECT * from ACCOUNTS where USERNAME="%s" and PASSWORD="%s"' % (
                check_username, check_passwd)).fetchone():
            print('login successful')
            updateStatus(text_field, f'[USER LOGIN] {address} - username:{check_username} successful')
            conn.send(SUCCESS.encode(FORMAT))
        else:
            conn.send(WRONG_PASS.encode(FORMAT))
    else:
        conn.send(USER_ERROR.encode(FORMAT))
    data.close()


def checkSignup(conn, new_user, new_passwd, address, text_field):
    # open database
    data = sqlite3.connect('accounts.db')
    cursor = data.execute('SELECT * from ACCOUNTS where USERNAME="%s"' % new_user)
    if cursor.fetchone():
        conn.send(USER_TAKEN.encode(FORMAT))
        print('this username has already taken.')
    else:
        data.execute('INSERT INTO ACCOUNTS(USERNAME,PASSWORD) VALUES (?, ?)', (new_user, new_passwd))
        data.commit()
        print('thanks for signing up')
        updateStatus(text_field, f'[USER SIGNUP] {address} - username:{new_user} successful')
        conn.send(SUCCESS.encode(FORMAT))
    data.close()


def getUser(conn):
    user = getData(conn)
    conn.send("username accepted".encode(FORMAT))
    passwd = getData(conn)
    conn.send("password accepted".encode(FORMAT))
    return user, passwd


def getData(conn):
    data_length = int(conn.recv(HEADER).decode(FORMAT))
    data = conn.recv(data_length).decode(FORMAT)
    return data


def getDate():
    return date.today().strftime(DATE_FORMAT)


def handle_client(conn, addr, text_field):
    print(f"[NEW CONNECTION] {addr}")
    updateStatus(text_field, f"[NEW CONNECTION] {addr}")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == LOGIN:
                updateStatus(text_field, f'[USER LOGIN] {addr} request')
                conn.send(LOGIN.encode(FORMAT))
                user, passwd = getUser(conn)
                checkLogin(conn, user, passwd, addr, text_field)

            if msg == SIGNUP:
                updateStatus(text_field, f'[USER SIGNUP] {addr} request')
                conn.send(SIGNUP.encode(FORMAT))
                user, passwd = getUser(conn)
                checkSignup(conn, user, passwd, addr, text_field)

            if msg == CONVERT:
                updateStatus(text_field, f'[USER CONVERT] {addr} request')
                conn.send(CONVERT.encode(FORMAT))
                CurrencyConverter(conn, text_field).convertHandle()

            if msg == DISCONNECT_MESSAGE:
                updateStatus(text_field, f'[USER DISCONNECTED] {addr}')
                connected = False

        except (ValueError, ConnectionResetError):
            updateStatus(text_field, f'[USER DISCONNECTED] {addr}')
            connected = False

    conn.close()


def start(sv, sv_addr, text_field):
    sv.listen()
    print(f"[LISTENING] Server is listening on {sv_addr}")
    updateStatus(text_field, "[LISTENING] Server is listening...")
    try:
        while True:
            conn, addr = sv.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, text_field))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print('Keyboard Interrupt: Force close!')
        sv.close()
    finally:
        print('Server closed')
        sv.close()


def config(ip_add, port, text_field):
    server_running = False
    addr = (ip_add, int(port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    updateStatus(text_field, f'[SERVER ADDRESS] {addr}')

    def all_point():
        nonlocal server_running
        start(server, addr, text_field)

    server_thread = threading.Thread(target=all_point, daemon=True)
    if not server_running:
        server_thread.start()


def updateStatus(text_field, text):
    text_field.config(state=tk.NORMAL)
    text_field.insert(tk.END, text + '\n')
    text_field.update()
    text_field.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = Server()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print('Keyboard Interrupt: Force close!')
