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

# option
LOGIN = 'login'
SIGNUP = 'signup'


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.loginUI(controller)

    def loginUI(self, controller):
        cb1 = tk.IntVar()

        def show_passw():
            if cb1.get() == 1:
                pass_entry.config(show='')
            else:
                pass_entry.config(show='*')

        login_label = tk.Label(self, text='Login')
        lf = tk.LabelFrame(self, text='Login')
        user_label = tk.Label(lf, text='Username')
        user_entry = tk.Entry(lf, textvariable=self.username, width=30)
        pass_label = tk.Label(lf, text='Password')
        pass_entry = tk.Entry(lf, textvariable=self.password, show='*', width=30)
        show_pass = tk.Checkbutton(lf, text='Show password', variable=cb1, onvalue=1, offvalue=0, command=show_passw)
        login_btn = tk.Button(lf, text='Login', width=25, command=self.login)
        signup_label = tk.Label(lf, text='Did''t have an account?')
        signup_btn = tk.Button(lf, text='Sign up', width=25,
                               command=lambda: controller.show_frame(SignUp))

        # show labels, entries and button
        login_label.pack()
        user_label.pack(anchor='w', padx=15, pady=(10, 0))
        user_entry.pack()
        pass_label.pack(anchor='w', padx=15, pady=(10, 0))
        pass_entry.pack()
        show_pass.pack(anchor='w', padx=15)
        login_btn.pack(pady=10)
        signup_label.pack()
        signup_btn.pack()
        lf.pack(ipadx=15, ipady=15, pady=20)

    def login(self):
        try:
            user = self.username.get()
            passwd = self.password.get()
            loginID = [user, passwd]
            if user == '' or passwd == '':
                messagebox.showerror('Error', 'Invalid Input')
            else:
                option = LOGIN
                send(option)
                send(user)
                send(passwd)

        except:
            messagebox.showerror('Error', 'Server is not responding')


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        self.signUpUI(controller)

    def signUpUI(self, controller):
        cb2 = tk.IntVar()

        def show_passw():
            if cb2.get() == 1:
                pass_entry.config(show='')
            else:
                pass_entry.config(show='*')

        signup_label = tk.Label(self, text='Sign Up')
        lf = tk.LabelFrame(self, text='Signup')
        user_label = tk.Label(lf, text='Username')
        user_entry = tk.Entry(lf, textvariable=self.username, width=30)
        pass_label = tk.Label(lf, text='Password')
        pass_entry = tk.Entry(lf, textvariable=self.password, show='*', width=30)
        show_pass = tk.Checkbutton(lf, text='Show password', variable=cb2, onvalue=1, offvalue=0, command=show_passw)
        cpass_label = tk.Label(lf, text='Confirm Password')
        cpass_entry = tk.Entry(lf, textvariable=self.confirm_pass, show='*', width=30)
        signup_btn = tk.Button(lf, text='Sign up', width=25, command=self.signup)
        cancel_btn = tk.Button(lf, text='Cancel', width=25, command=lambda: controller.show_frame(Login))
        # show everything
        signup_label.pack()
        user_label.pack(anchor='w', padx=15, pady=(10, 0))
        user_entry.pack()
        pass_label.pack(anchor='w', padx=15, pady=(10, 0))
        pass_entry.pack()
        show_pass.pack(anchor='w', padx=15)
        cpass_label.pack(anchor='w', padx=15, pady=(10, 0))
        cpass_entry.pack()
        signup_btn.pack(pady=(20, 10))
        cancel_btn.pack()
        lf.pack(ipadx=15, ipady=15, pady=20)

    def signup(self):
        if self.username.get() == '' or self.password.get() == '' or self.confirm_pass.get() == '':
            messagebox.showerror('Error', 'Invalid Input')
        else:
            passw = self.password.get()
            confirm_passw = self.confirm_pass.get()
            if passw != confirm_passw:
                messagebox.showerror('Error', 'The password confirmation does not match.')


class Connect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
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

        # creating labels and entries
        noti_label = tk.Label(self, text='Please enter detail below', bg='#00a2ed', fg='white')
        lb = tk.LabelFrame(self, text='Connect')
        ip_label = tk.Label(lb, text='IP Address', )
        ip_entry = tk.Entry(lb, textvariable=self.ip)
        port_label = tk.Label(lb, text='Port')
        port_entry = tk.Entry(lb, textvariable=self.port)

        # print button and check button
        auto_cb = tk.Checkbutton(lb, text='Automatic', variable=cb, onvalue=1, offvalue=0, command=isChecked)
        connect_bt = tk.Button(lb, text='Connect', command=self.submit)

        # print labels end entries
        noti_label.pack(fill=tk.X)
        ip_label.pack(pady=5)
        ip_entry.pack(ipadx=15)
        port_label.pack(pady=5)
        port_entry.pack(ipadx=15)
        auto_cb.pack(pady=5)
        connect_bt.pack(ipadx=15, pady=15)
        lb.pack(ipadx=15, ipady=5, pady=20)

    def connect_server(self):
        addr = (self.ip.get(), int(self.port.get()))
        client.connect(addr)

    def submit(self):
        print(self.ip.get())
        print(self.port.get())
        if self.ip.get() == '' or self.port.get() == '':
            messagebox.showerror('Error', 'Invalid Input')
        else:
            try:
                self.connect_server()
                if messagebox.showinfo('Connected', 'Connected successfully!'):
                    self.destroy()
            except socket.error:
                messagebox.showerror('Error', 'Connection error')


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def AppUI(self):
        intro_label = tk.Label(self, text='Real Time Currency Converter',
                               bg='dodgerblue2', relief=tk.RAISED, borderwidth=3)
        intro_label.config(font=('Courier', 15, 'bold'))
        # date_label = tk.Label(self, text='12-10-2021', relief=tk.GROOVE, borderwidth=5)


class UI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('420x450+500+300')
        self.resizable(width=False, height=False)
        # self.protocol('WM_DELETE_WINDOW', self.on_closing)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Connect, Login):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.frames[Connect].tkraise()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # def on_closing(self):
    #     if messagebox.askokcancel('Quit', 'Are you want to quit?'):
    #         self.destroy()


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app = UI()
    app.mainloop()
