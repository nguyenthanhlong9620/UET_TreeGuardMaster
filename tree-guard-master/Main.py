from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import tkinter as tk
from tkinter import font as tkfont

from pip._vendor.cachecontrol import controller

with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
db.commit()
db.close()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login", font=controller.title_font)
        label.grid(row=0, columnspan=2)

        self.username = StringVar()
        self.password = StringVar()

        self.label1 = Label(self, text='Username: ',
                            font=('', 20), pady=5, padx=5)
        self.entry1 = tk.Entry(
            self, textvariable=self.username, bd=5, font=('', 15))
        self.label2 = tk.Label(self, text='Password: ',
                               font=('', 20), pady=5, padx=5)
        self.entry2 = tk.Entry(
            self, textvariable=self.password, bd=5, font=('', 15), show='*')
        self.button1 = tk.Button(self, text="Login", bd=3, font=('', 15), padx=5, pady=5,
                                 command=self.check_log)
        self.button2 = tk.Button(self, text="Create Account", bd=3, font=('', 15), padx=5, pady=5,
                                 command=lambda: controller.show_frame("PageOne"))
        self.label1.grid(sticky=W)
        self.entry1.grid(row=1, column=1)
        self.label2.grid(sticky=W)
        self.entry2.grid(row=2, column=1)
        self.button1.grid()
        self.button2.grid(row=3, column=1)

    def check_log(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        global user
        user = self.username.get()
        if result:
            SampleApp.show_frame(self.controller, 'PageTwo')
        else:
            ms.showerror('Ooops', 'Username not found')


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Register", font=controller.title_font)
        label.grid(row=0, columnspan=2)

        self.n_username = StringVar()
        self.n_password = StringVar()

        self.label1 = Label(self, text='Username: ',
                            font=('', 20), pady=5, padx=5)
        self.entry1 = tk.Entry(
            self, textvariable=self.n_username, bd=5, font=('', 15))
        self.label2 = tk.Label(self, text='Password: ',
                               font=('', 20), pady=5, padx=5)
        self.entry2 = tk.Entry(
            self, textvariable=self.n_password, bd=5, font=('', 15), show='*')

        self.button = tk.Button(self, text="Register", bd=3, font=('', 15), padx=5, pady=5,
                                command=self.check_in)
        self.button2 = tk.Button(self, text="Go to Login", bd=3, font=('', 15), padx=5, pady=5,
                                 command=lambda: controller.show_frame("StartPage"))

        self.label1.grid(sticky=W)
        self.entry1.grid(row=1, column=1)
        self.label2.grid(sticky=W)
        self.entry2.grid(row=2, column=1)
        self.button.grid()
        self.button2.grid(row=3, column=1)

    def check_in(self):
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        find_user = ('SELECT username FROM user WHERE username = ?')
        c.execute(find_user, [(self.n_username.get())])

        if c.fetchall():
            ms.showerror('Error!', 'Username Taken, Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created!')
            SampleApp.show_frame(self.controller, 'PageTwo')

        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        db.commit()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="LogOut",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        button = tk.Button(self, text="Register new Account",
                           command=lambda: controller.show_frame("PageOne"))
        button.pack()
        self.button2 = tk.Button(self, command=self.change_text)
        self.button2.pack()

    def change_text(self):
        print('abc123')
        print(user)
        print(type(user))
        self.button2['text'] = user


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
