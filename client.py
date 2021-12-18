""" All currencies' data belong to ExchangeRate-API and
European Central Bank"""

# project socket "Mang may tinh"
# 20120401 - Nguyen Duc Viet
# 20CT3

import socket
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
from tkcalendar import DateEntry

# constant values
HEADER = 64
PORT = 6969
FORMAT = 'utf-8'
DATE_FORMAT = "%#m/%#d/%Y"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

# option
LOGIN = 'login'
SIGNUP = 'signup'
CONVERT = 'converter'
SUCCESS = 'Successful'
WRONG_PASS = 'Wrong password'
USER_ERROR = 'Username does not exist'
USER_TAKEN = 'Username has already taken'
CONNECTION_ERROR = 'Server is not responding.'

# color constants
BG_COLOR = 'ghostwhite'
LIGHT_BLUE = '#4BB4DE'
MID_BLUE = '#3B8AC4'
DARK_BLUE = '#345DA7'


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.loginUI(controller)

    def loginUI(self, controller):
        username = tk.StringVar()
        password = tk.StringVar()
        cb1 = tk.IntVar()

        def show_passw():
            if cb1.get() == 1:
                pass_entry.config(show='')
            else:
                pass_entry.config(show='*')

        def login():
            try:
                user = username.get()
                passwd = password.get()
                if user == '' or passwd == '':
                    error_entry.config(text='Invalid input')
                else:
                    if send(LOGIN) == LOGIN:
                        print(send(user))
                        print(send(passwd))
                        error = server_response()
                        if error == USER_ERROR:
                            error_entry.config(text=USER_ERROR)
                        elif error == WRONG_PASS:
                            error_entry.config(text=WRONG_PASS)
                        else:
                            messagebox.showinfo('Login', SUCCESS)
                            controller.show_frame(App)

            except ConnectionResetError:
                messagebox.showerror('Error', CONNECTION_ERROR)
                controller.show_frame(Connect)

        self.configure(background=BG_COLOR)
        login_label = tk.Label(self, text='Currency Converter', bg='dodgerblue1', fg=BG_COLOR)
        login_label.config(font=('Helvetica', 17, 'bold'))
        lf = tk.LabelFrame(self, text='Login', bg=BG_COLOR, foreground=DARK_BLUE)
        user_label = tk.Label(lf, text='Username', bg=BG_COLOR)
        user_entry = tk.Entry(lf, textvariable=username, width=30, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        pass_label = tk.Label(lf, text='Password', bg=BG_COLOR)
        pass_entry = tk.Entry(lf, textvariable=password, show='*', width=30, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        show_pass = tk.Checkbutton(lf, text='Show password', variable=cb1, onvalue=1, offvalue=0, command=show_passw,
                                   activebackground=BG_COLOR, bg=BG_COLOR)
        error_entry = tk.Label(lf, bg=BG_COLOR, fg='firebrick1')
        login_btn = tk.Button(lf, text='Login', width=25, command=login, bg=MID_BLUE, fg='white', borderwidth=2,
                              activebackground=BG_COLOR, activeforeground=MID_BLUE)
        signup_label = tk.Label(lf, text='Did''t have an account?', bg=BG_COLOR)
        signup_btn = tk.Button(lf, text='Sign up', width=25,
                               command=lambda: controller.show_frame(SignUp), bg=MID_BLUE, fg='white', borderwidth=2,
                               activebackground=BG_COLOR, activeforeground=MID_BLUE)

        # show labels, entries and button
        login_label.pack(fill=tk.BOTH)
        user_label.pack(anchor='w', padx=15, pady=(10, 0))
        user_entry.pack()
        pass_label.pack(anchor='w', padx=15, pady=(10, 0))
        pass_entry.pack()
        show_pass.pack(anchor='w', padx=15)
        error_entry.pack(pady=(10, 0))
        login_btn.pack(pady=10)
        signup_label.pack()
        signup_btn.pack()
        lf.pack(ipadx=15, ipady=15, pady=20)


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.signUpUI(controller)

    def signUpUI(self, controller):
        username = tk.StringVar()
        password = tk.StringVar()
        confirm_pass = tk.StringVar()
        cb2 = tk.IntVar()

        def show_passw():
            if cb2.get() == 1:
                pass_entry.config(show='')
            else:
                pass_entry.config(show='*')

        def signup():
            user = username.get()
            passwd = password.get()
            conf_passwd = confirm_pass.get()
            if user == '' or passwd == '' or conf_passwd == '':
                noti_label.config(text='Invalid input')
            else:
                if passwd != conf_passwd:
                    noti_label.config(text='Password does not match.')
                else:
                    try:
                        if send(SIGNUP) == SIGNUP:
                            print(send(user))
                            print(send(passwd))
                            error = server_response()
                            if error == USER_TAKEN:
                                noti_label.config(text=USER_TAKEN)
                            else:
                                messagebox.showinfo('Sign up', SUCCESS)
                                controller.show_frame(Login)
                    except ConnectionResetError:
                        messagebox.showerror('Error', CONNECTION_ERROR)
                        controller.show_frame(Connect)

        # widgets
        self.config(bg=BG_COLOR)
        signup_label = tk.Label(self, text='Currency Converter', bg='dodgerblue1', fg='white')
        signup_label.config(font=('Helvetica', 17, 'bold'))
        lf = tk.LabelFrame(self, text='Signup', bg=BG_COLOR, foreground=DARK_BLUE)
        user_label = tk.Label(lf, text='Username', bg=BG_COLOR)
        user_entry = tk.Entry(lf, textvariable=username, width=30, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        pass_label = tk.Label(lf, text='Password', bg=BG_COLOR)
        pass_entry = tk.Entry(lf, textvariable=password, show='*', width=30, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        show_pass = tk.Checkbutton(lf, text='Show password', variable=cb2, onvalue=1, offvalue=0, command=show_passw,
                                   activebackground=BG_COLOR, bg=BG_COLOR)
        cpass_label = tk.Label(lf, text='Confirm Password', bg=BG_COLOR)
        cpass_entry = tk.Entry(lf, textvariable=confirm_pass, show='*', width=30, highlightthickness=2,
                               highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        noti_label = tk.Label(lf, bg=BG_COLOR, fg='firebrick1')
        signup_btn = tk.Button(lf, text='Sign up', width=25, command=signup, bg=MID_BLUE, fg='white', borderwidth=2,
                               activebackground=BG_COLOR, activeforeground=MID_BLUE, disabledforeground=MID_BLUE)
        cancel_btn = tk.Button(lf, text='Cancel', width=25, command=lambda: controller.show_frame(Login),
                               bg=MID_BLUE, fg='white', borderwidth=2,
                               activebackground=BG_COLOR, activeforeground=MID_BLUE, disabledforeground=MID_BLUE)
        # show everything
        signup_label.pack(fill=tk.BOTH)
        user_label.pack(anchor='w', padx=15, pady=(10, 0))
        user_entry.pack()
        pass_label.pack(anchor='w', padx=15, pady=(10, 0))
        pass_entry.pack()
        show_pass.pack(anchor='w', padx=15)
        cpass_label.pack(anchor='w', padx=15, pady=(10, 0))
        cpass_entry.pack()
        noti_label.pack(pady=5)
        signup_btn.pack(pady=(20, 10))
        cancel_btn.pack()
        lf.pack(ipadx=15, ipady=15, pady=20)


class Connect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.controller = controller
        self.connectUI()

    def connectUI(self):
        cb = tk.IntVar()

        def isChecked():
            if cb.get() == 1:
                ip_entry.delete(0, 'end')
                port_entry.delete(0, 'end')
                ip_entry.insert(0, SERVER)
                port_entry.insert(0, str(PORT))
                ip_entry.config(state='disabled')
                port_entry.config(state='disabled')
            elif cb.get() == 0:
                ip_entry.config(state="normal")
                port_entry.config(state="normal")
                ip_entry.delete(0, 'end')
                port_entry.delete(0, 'end')

        # creating labels and entry boxes
        self.configure(background=BG_COLOR)
        noti_label = tk.Label(self, text='Please enter detail below', bg='#00a2ed', fg=BG_COLOR)
        lb = tk.LabelFrame(self, text='Connect', fg=DARK_BLUE, bg=BG_COLOR)
        ip_label = tk.Label(lb, text='IP Address', bg=BG_COLOR)
        ip_entry = tk.Entry(lb, textvariable=self.ip, highlightthickness=2,
                            highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)
        port_label = tk.Label(lb, text='Port', bg=BG_COLOR)
        port_entry = tk.Entry(lb, textvariable=self.port, highlightthickness=2,
                              highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)

        # print button and check button
        auto_cb = tk.Checkbutton(lb, text='Automatic', variable=cb, onvalue=1, offvalue=0, command=isChecked,
                                 bg=BG_COLOR, activebackground=BG_COLOR)
        connect_bt = tk.Button(lb, text='Connect', command=self.submit, bg=MID_BLUE, fg='white', borderwidth=2,
                               activebackground=BG_COLOR, activeforeground=MID_BLUE)

        # print labels end entries
        noti_label.pack(fill=tk.X)
        ip_label.pack(pady=5)
        ip_entry.pack(ipadx=15)
        port_label.pack(pady=5)
        port_entry.pack(ipadx=15)
        auto_cb.pack(pady=5)
        connect_bt.pack(ipadx=15, pady=15)
        lb.pack(ipadx=15, ipady=5, pady=20)

    def submit(self):
        print(self.ip.get())
        print(self.port.get())
        if self.ip.get() == '' or self.port.get() == '':
            messagebox.showerror('Error', 'Invalid Input')
        else:
            try:
                connect_server(self.ip.get(), int(self.port.get()))
                if messagebox.showinfo('Connected', 'Connected successfully!'):
                    # self.destroy()
                    self.controller.show_frame(Login)
            except socket.error:
                messagebox.showerror('Error', 'Server is not responding.')


class App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.currencies = ["USD", "EUR", "JPY", "AUD", "CAD", "CNY", "HKD",
                           "NZD", "KRW", "SGD", "INR", "RUB", "THB", "VND"]
        custom_font = 'Helvetica, 11'

        # header frame
        self.config(bg=BG_COLOR)
        header_lf = tk.Frame(self, bg=BG_COLOR)
        intro_label = tk.Label(header_lf, text='Currency Converter', bg='dodgerblue1', fg='white')
        intro_label.config(font=('Helvetica', 17, 'bold'))
        date_label = tk.Label(header_lf, text='Pick A Date', bg=BG_COLOR)
        date_label.config(font=custom_font)
        self.cal = DateEntry(header_lf, width=16, background="dodgerblue1", foreground="white", bd=2, state='readonly')
        self.cal.config(mindate=datetime.date(year=2021, month=7, day=7), maxdate=datetime.date.today())
        intro_label.pack(pady=5, fill=tk.BOTH)
        date_label.pack(pady=5)
        self.cal.pack(pady=(0, 10))
        header_lf.pack(fill=tk.BOTH)

        self.from_currency_variable = tk.StringVar()
        self.from_currency_variable.set("EUR")  # default value
        self.to_currency_variable = tk.StringVar()
        self.to_currency_variable.set("USD")  # default value

        # drop down
        main_frame = tk.Frame(self, bg=BG_COLOR)

        self.from_currency_dropdown = ttk.Combobox(main_frame, textvariable=self.from_currency_variable,
                                                   values=self.currencies,
                                                   state='readonly', width=10, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(main_frame, textvariable=self.to_currency_variable,
                                                 values=self.currencies,
                                                 state='readonly', width=10, justify=tk.CENTER)

        # main_frame
        field_label = tk.Label(main_frame, text='Enter Amount To Convert', bg=BG_COLOR)
        field_label.config(font=custom_font)
        from_label = tk.Label(main_frame, text='From', bg=BG_COLOR)
        to_label = tk.Label(main_frame, text='To', bg=BG_COLOR)
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = tk.Entry(main_frame, justify=tk.CENTER, validate='key', validatecommand=valid, width=40,
                                     highlightthickness=2, highlightcolor=MID_BLUE, highlightbackground=BG_COLOR)

        self.convert_bt = tk.Button(main_frame, text='Convert', bd=1, bg='dodgerblue1', fg='white',
                                    activebackground=BG_COLOR, width=30, command=lambda: self.perform(controller))
        self.converted = tk.Label(self, text='', font=('Helvetica', '17'), bg=BG_COLOR)
        self.currency_info = tk.Label(self, text='', font=custom_font, bg=BG_COLOR)

        # show all widgets
        field_label.grid(row=0, column=0, columnspan=2, pady=5, padx=30)
        self.amount_field.grid(row=1, column=0, columnspan=2, pady=(0, 5), padx=30)
        from_label.grid(row=2, column=0, sticky='w', padx=50)
        to_label.grid(row=2, column=1, sticky='e', padx=60)
        self.from_currency_dropdown.grid(row=3, column=0, sticky='w', padx=(30, 0))
        self.to_currency_dropdown.grid(row=3, column=1, sticky='e', padx=(0, 30))
        self.convert_bt.grid(row=4, column=0, columnspan=2, pady=20)
        main_frame.pack()

        self.converted.pack(pady=20)
        self.currency_info.pack(pady=(30, 0))

        # return to log in screen
        logout_bt = tk.Button(self, text='Logout', width=15, bd=1, bg='dimgray', fg='white',
                              command=lambda: return_login(controller))
        logout_bt.pack(pady=(20, 0))

        def return_login(control):
            control.show_frame(Login)

    def perform(self, controller):
        try:
            print(send(CONVERT))
            print(self.cal.get_date().strftime(DATE_FORMAT))
            send(self.cal.get_date().strftime(DATE_FORMAT))
            send(self.from_currency_variable.get())
            send(self.to_currency_variable.get())
            send(self.amount_field.get())
            data = server_response()
            base_data = server_response()
            self.converted.config(text=data + ' ' + self.to_currency_variable.get())
            self.currency_info.config(text='1 ' + self.from_currency_variable.get() + ' = ' + base_data + ' '
                                           + self.to_currency_variable.get())
        except (ConnectionResetError, OSError):
            messagebox.showerror('Error', CONNECTION_ERROR)
            controller.show_frame(Connect)

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"^(?=.*?\d)\d*[.,]?\d*$")
        result = regex.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)


class UI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('420x450+500+300')
        self.resizable(width=False, height=False)
        self.title('Currency Converter: Client')
        logo = tk.PhotoImage(file='logo.png')
        self.iconphoto(False, logo)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Connect, Login, SignUp, App):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # show first frame
        self.frames[Connect].tkraise()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel('Quit', 'Are you want to quit?'):
            self.destroy()


def connect_server(ip, port):
    addr = (ip, port)
    client.connect(addr)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return server_response()


def server_response():
    return str(client.recv(2048).decode(FORMAT))


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app = UI()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print('Keyboard Interrupt: Force close!')
