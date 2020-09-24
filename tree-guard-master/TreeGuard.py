import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import messagebox as ms, filedialog
import random
from PIL import Image, ImageTk
import tkinter.filedialog
import serial
from time import sleep

with sqlite3.connect('quit.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL);')
db.commit()

c.execute(
    'CREATE TABLE IF NOT EXISTS node (point_x INTEGER NOT NULL, point_y INTEGER NOT NULL, status INTEGER NOT NULL, id INTEGER NOT NULL);')
db.commit()

c.execute(
    'CREATE TABLE IF NOT EXISTS map (path TEXT NOT NULL, coord_x INTEGER NOT NULL, coord_y INTEGER NOT NULL, NW_coordX INTEGER NOT NULL, NW_coordY INTEGER NOT NULL);')
db.commit()

db.close()


class MainFrame:
    def __init__(self, root):
        self.root = root
        self.widget()

    def widget(self):
        root.title('Main Screen')
        root.geometry('980x540')
        File = 'background.jpg'

        self.bg = ImageTk.PhotoImage(Image.open(File).resize((980, 540), Image.ANTIALIAS))
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.frame1 = tk.Frame(self.root)
        self.frame1.place(x=100, y=100, height=200, width=530)

        title = tk.Label(self.frame1, text='WELCOME TO UET-TREEGUARD SYSTEM', font=('Impact', 25, 'bold')).place(x=0,
                                                                                                                 y=0)
        login_here = tk.Label(self.frame1, text='LOGIN HERE ', font=('Times New Roman', 15, 'bold')).place(x=0, y=70)
        register_here = tk.Label(self.frame1, text='REGISTER HERE', font=('Times New Roman', 15, 'bold')).place(x=0,
                                                                                                                y=140)

        button_register = tk.Button(self.frame1, text='Register ', font=('Times New Roman', 15),
                                    command=self.hideToLogin).place(x=200, y=135)
        button_login = tk.Button(self.frame1, text='Login', font=('Times New Roman', 15),
                                 command=self.hideToRegister).place(x=200, y=65)

    def hideToLogin(self):
        self.bg = None
        self.frame1.destroy()
        LoginFrame(root)

    def hideToRegister(self):
        self.bg = None
        self.frame1.destroy()
        RegisterFrame(root)


class LoginFrame:  # ngược
    def __init__(self, root):
        self.root = root
        self.widget()

    def widget(self):
        self.username = StringVar()
        self.password = StringVar()

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack()
        root.geometry('500x200')
        root.title('Register')

        self.label_start = tk.Label(self.frame2, text='REGISTER HERE', font=('Times New Roman', 25, 'bold'))
        self.label_user = tk.Label(self.frame2, text='Username: ', font=('', 20), padx=5, pady=5)
        self.entry_user = tk.Entry(self.frame2, textvariable=self.username, bd=5, font=('', 15))
        self.label_pass = tk.Label(self.frame2, text='Password: ', font=('', 20), padx=5, pady=5)
        self.entry_pass = tk.Entry(self.frame2, textvariable=self.password, bd=5, font=('', 15), show='*')

        self.button_main_screen = tk.Button(self.frame2, text='Register', command=self.hideToMain)

        self.label_start.grid(row=0, columnspan=2)
        self.label_user.grid(row=1)
        self.entry_user.grid(row=1, column=1)
        self.label_pass.grid(sticky=W)
        self.entry_pass.grid(row=2, column=1)
        self.button_main_screen.grid(row=3, column=1)

    def hideToMain(self):
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        find_user = ('SELECT username FROM user WHERE username = ?')
        c.execute(find_user, [(self.username.get())])

        if c.fetchall():
            ms.showerror('Error!', 'Username Taken, Try a Diffrent One.')
        else:
            ms.showinfo('Success!', 'Account Created!')

            self.frame2.pack_forget()
            MainFrame(root)

        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        c.execute(insert, [(self.username.get()), (self.password.get())])
        db.commit()


class RegisterFrame:  # ngược
    def __init__(self, root):
        self.root = root
        self.widget()

    def widget(self):
        self.frame3 = tk.Frame(self.root)
        self.frame3.pack()
        root.geometry('500x200')
        root.title('Login')

        self.n_username = StringVar()
        self.n_password = StringVar()

        self.label_start = tk.Label(self.frame3, text='LOGIN HERE', font=('Times New Roman', 25, 'bold'))
        self.label_user = tk.Label(self.frame3, text='Username: ', font=('', 20), padx=5, pady=5)
        self.entry_user = tk.Entry(self.frame3, textvariable=self.n_username, bd=5, font=('', 15))
        self.label_pass = tk.Label(self.frame3, text='Password: ', font=('', 20), padx=5, pady=5)
        self.entry_pass = tk.Entry(self.frame3, textvariable=self.n_password, bd=5, font=('', 15), show='*')
        self.button_main_screen2 = tk.Button(self.frame3, text='Login', command=self.hidetoMain2)

        self.label_start.grid(row=0, columnspan=2)
        self.label_user.grid(row=1)
        self.entry_user.grid(row=1, column=1)
        self.label_pass.grid(sticky=W)
        self.entry_pass.grid(row=2, column=1)
        self.button_main_screen2.grid(row=3, column=1)

    def hidetoMain2(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.n_username.get()), (self.n_password.get())])
        result = c.fetchall()

        if result:
            self.frame3.pack_forget()
            # MainFrame(root)
            ShowData(root)
        else:
            ms.showerror('Ooops', 'Username not found')


class ShowData:
    def __init__(self, root):
        self.root = root
        self.widget()
        self.children_dictX = dict()
        self.children_dictY = dict()
        self.children_NW_X = dict()
        self.children_NW_Y = dict()
        self.children_X = dict()
        self.children_Y = dict()
        self.children_ID = dict()

    lat = 0
    lon = 0
    global arr
    arr = []
    global arr_point
    arr_point = []
    global sourceFile
    sourceFile = ''

    def widget(self):
        self.frame4 = tk.Frame(self.root, bd=2, relief=SUNKEN)
        self.frame4.grid_rowconfigure(0, weight=2)
        self.frame4.grid_columnconfigure(0, weight=2)

        xscroll = tk.Scrollbar(self.frame4, orient=HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky=E + W)
        yscroll = tk.Scrollbar(self.frame4)
        yscroll.grid(row=0, column=1, sticky=N + S)
        root.geometry('350x350')
        root.title('UET-TreeGuard')

        global canvas
        canvas = tk.Canvas(self.frame4, bd=0, xscrollcommand=xscroll.set,
                           yscrollcommand=yscroll.set)
        canvas.grid(row=0, column=0, sticky=N + S + E + W)

        canvas.bind("<ButtonPress-1>", self.printcoords)

        xscroll.config(command=canvas.xview)
        yscroll.config(command=canvas.yview)

        button_add = tk.Button(root, text='Add', command=self.handleAddButton)
        button_delete = tk.Button(root, text='Delete', command=self.handleDeleteButton)
        button_signal = tk.Button(root, text='Get Signal', command=self.handleSignal)
        button_changeMap = tk.Button(root, text='Change Map', command=self.changeMap)
        button_add.pack(side='bottom')
        button_delete.pack(side='bottom')
        button_signal.pack(side='bottom')
        button_changeMap.pack(side='bottom')

        self.frame4.pack(fill=BOTH, expand=1)

        self.loadDB()

    def loadDB(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()

        c.execute('SELECT * FROM map')
        load_map = c.fetchall()

        for x in load_map:
            File = x[0]
            self.img = ImageTk.PhotoImage(Image.open(File))
            canvas.create_image(0, 0, image=self.img, anchor=NW)
            canvas.image = self.img
            canvas.config(scrollregion=canvas.bbox(ALL))

        c.execute('SELECT * FROM node')
        ans = c.fetchall()

        for x in ans:
            if (x[2] == 0):
                old_rectangle = canvas.create_rectangle(x[0] - 10, x[1] - 10, x[0] + 10, x[1] + 10, fill='gray')
                arr_point.append(old_rectangle)
            else:
                signal_rectangle = canvas.create_rectangle(x[0] - 10, x[1] - 10, x[0] + 10, x[1] + 10, fill='blue')
                arr_point.append((signal_rectangle))

        self.signal_data()

    def signal_data(self):

        data = self.get_data()

        with sqlite3.connect('quit.db') as db:

            # create cursor

            c = db.cursor()

        c.execute('SELECT * FROM node')

        ans = c.fetchall()

        for x in arr_point:

            for y in ans:

                if(y[0] >= int(canvas.coords(x)[0]) and y[0] <= int(canvas.coords(x)[2]) and

                    y[1] >= int(canvas.coords(x)[1]) and y[1] <= int(canvas.coords(x)[3])):

                    k = str(y[3])
                    if (data == bytes(k,'utf-8')):
                        canvas.itemconfig(x, fill='red')
                    else:
                        canvas.itemconfig(x, fill='blue')

        root.after(500, self.signal_data)

    def get_data(self):
        #data = random.randint(1, 5)

        received_data = ser.read()         
        sleep(0.1)
        data_left = ser.inWaiting()               
        received_data += ser.read(data_left)
        #print("Data ", received_data)
        return received_data
        
        #return data

    def changeMap(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()

        sourceFile = filedialog.askopenfilename(parent=root, initialdir="/", title='Please select a directory')

        delete_map = 'DELETE FROM map'
        c.execute(delete_map)
        db.commit()

        delete_nodes = 'DELETE FROM node'
        c.execute(delete_nodes)
        db.commit()

        insert = 'INSERT INTO map(path, coord_x, coord_y, NW_coordX, NW_coordY) VALUES(?,?,?,?,?)'
        c.execute(insert, [sourceFile, 100, 100, 0, 0])
        db.commit()

        add_coordForMap = tk.Toplevel()
        add_coordForMap.title('Input Position')

        add_coordForMap.itemX = IntVar()
        add_coordForMap.itemY = IntVar()
        add_coordForMap.NW_X = IntVar()
        add_coordForMap.NW_Y = IntVar()

        add_coordForMap.label_getCoordsX = tk.Label(add_coordForMap, text='SE_Coord X', font=('', 15), padx=5, pady=5)
        add_coordForMap.entry_getCoordsX = tk.Entry(add_coordForMap, textvariable=add_coordForMap.itemX, bd=5,
                                                    font=('', 10))
        add_coordForMap.label_getCoordsY = tk.Label(add_coordForMap, text='SE_Coord Y', font=('', 15), padx=5, pady=5)
        add_coordForMap.entry_getCoordsY = tk.Entry(add_coordForMap, textvariable=add_coordForMap.itemY, bd=5,
                                                    font=('', 10))

        add_coordForMap.label_NW_X = tk.Label(add_coordForMap, text='NW_Coord X', font=('', 15), padx=5, pady=5)
        add_coordForMap.entry_NW_X = tk.Entry(add_coordForMap, textvariable=add_coordForMap.NW_X, bd=5, font=('', 10))
        add_coordForMap.label_NW_Y = tk.Label(add_coordForMap, text='NW_Coord Y', font=('', 15), padx=5, pady=5)
        add_coordForMap.entry_NW_Y = tk.Entry(add_coordForMap, textvariable=add_coordForMap.NW_Y, bd=5, font=('', 10))

        self.children_dictX[add_coordForMap] = add_coordForMap.itemX
        self.children_dictY[add_coordForMap] = add_coordForMap.itemY

        self.children_NW_X[add_coordForMap] = add_coordForMap.NW_X
        self.children_NW_Y[add_coordForMap] = add_coordForMap.NW_Y

        add_coordForMap.label_getCoordsX.grid(row=0, column=0)
        add_coordForMap.entry_getCoordsX.grid(row=0, column=1)
        add_coordForMap.label_getCoordsY.grid(row=1, column=0)
        add_coordForMap.entry_getCoordsY.grid(row=1, column=1)
        add_coordForMap.label_NW_X.grid(row=2, column=0)
        add_coordForMap.entry_NW_X.grid(row=2, column=1)
        add_coordForMap.label_NW_Y.grid(row=3, column=0)
        add_coordForMap.entry_NW_Y.grid(row=3, column=1)
        add_coordForMap.button_getCoords = tk.Button(add_coordForMap, text='Accept',
                                                     command=lambda: self.confirmCoords(add_coordForMap))
        add_coordForMap.button_getCoords.grid(row=4, columnspan=2)

        self.File = sourceFile
        self.img = ImageTk.PhotoImage(Image.open(self.File))
        canvas.create_image(0, 0, image=self.img, anchor=NW)
        canvas.image = self.img
        canvas.config(scrollregion=canvas.bbox(ALL))

        c.execute('SELECT * FROM map')
        ans = c.fetchall()
        for x in ans:
            print(x)

    def confirmCoords(self, add_coordForMap):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()

        x = self.children_dictX[add_coordForMap].get()
        y = self.children_dictY[add_coordForMap].get()
        NW_x = self.children_NW_X[add_coordForMap].get()
        NW_y = self.children_NW_Y[add_coordForMap].get()

        update_id = 'UPDATE map SET coord_x=? WHERE path=?'
        c.execute(update_id, (x, self.File))
        db.commit()

        update_id = 'UPDATE map SET coord_y=? WHERE path=?'
        c.execute(update_id, (y, self.File))
        db.commit()

        update_id = 'UPDATE map SET NW_coordX=? WHERE path=?'
        c.execute(update_id, (NW_x, self.File))
        db.commit()

        update_id = 'UPDATE map SET NW_coordY=? WHERE path=?'
        c.execute(update_id, (NW_y, self.File))
        db.commit()

        c.execute('SELECT * FROM map')
        ans = c.fetchall()
        for x in ans:
            print(x[0])

        add_coordForMap.destroy()

    def printcoords(self, event):
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)
        global lat
        global lon
        global location
        lat = cy
        lon = cx

        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()
        c.execute('SELECT * FROM map')
        ans = c.fetchall()
        for x in ans:
            print(x)
        print(cx)
        print(cy)

        File = 'location.png'
        self.img_location = ImageTk.PhotoImage(Image.open(File).resize((20, 20), Image.ANTIALIAS))

        if len(arr) == 0:
            location = canvas.create_image(lon - 10, lat - 10, image=self.img_location, anchor="nw")
            canvas.image = self.img_location
            arr.append(location)
        else:
            canvas.delete(location)
            arr.remove(arr[0])
            location = canvas.create_image(lon - 10, lat - 10, image=self.img_location, anchor="nw")
            canvas.image = self.img_location
            arr.append(location)

    def handleAddButton(self):

        new_window = tk.Toplevel()
        new_window.title('Get ID')

        new_window.X = IntVar()
        new_window.Y = IntVar()
        new_window.ID = IntVar()

        new_window.label_EntryX = tk.Label(new_window, text='Coord X:', font=('', 15), padx=5, pady=5)
        new_window.entry_X = tk.Entry(new_window, textvariable=new_window.X, bd=5, font=('', 10))
        new_window.label_EntryY = tk.Label(new_window, text='Coord Y:', font=('', 15), padx=5, pady=5)
        new_window.entry_Y = tk.Entry(new_window, textvariable=new_window.Y, bd=5, font=('', 10))
        new_window.label_ID = tk.Label(new_window, text='ID: ', font=('', 15), padx=5, pady=5)
        new_window.entry_ID = tk.Entry(new_window, textvariable=new_window.ID, bd=5, font=('', 10))

        self.children_X[new_window] = new_window.X
        self.children_Y[new_window] = new_window.Y
        self.children_ID[new_window] = new_window.ID

        new_window.label_EntryX.grid(row=0, column=0)
        new_window.entry_X.grid(row=0, column=1)
        new_window.label_EntryY.grid(row=1, column=0)
        new_window.entry_Y.grid(row=1, column=1)
        new_window.label_ID.grid(row=3, column=0)
        new_window.entry_ID.grid(row=3, column=1)

        new_window.button_X_Y_ID = tk.Button(new_window, text='Accept', command=lambda: self.hideEntryID(new_window))
        new_window.button_X_Y_ID.grid(row=4, columnspan=2)

    def hideEntryID(self, new_window):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()
        x = self.children_X[new_window].get()
        y = self.children_Y[new_window].get()
        id = self.children_ID[new_window].get()

        c.execute('SELECT * FROM map')
        ans = c.fetchall()
        _x = ans[0][1]
        _y = ans[0][2]
        _NW_x = ans[0][3]
        _NW_y = ans[0][4]
        db.commit()

        insert = 'INSERT INTO node(point_x,point_y,status,id) VALUES(?,?,?,?)'
        c.execute(insert, [x - _NW_x, y - _NW_y, 0, id])
        db.commit()

        global rectangle

        a = abs(x - _NW_x) - 10
        b = abs(y - _NW_y) - 10
        c = abs(x - _NW_x) + 10
        d = abs(y - _NW_y) + 10

        rectangle = canvas.create_rectangle((a, b, c, d), fill='black')
        arr_point.append(rectangle)
        new_window.destroy()

    def handleSignal(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()
        if len(arr) != 0:
            canvas.delete(location)

        for x in arr_point:
            if (lon >= canvas.coords(x).pop(0) and lon <= canvas.coords(x).pop(2) and
                    lat >= canvas.coords(x).pop(1) and lat <= canvas.coords(x).pop(3)):
                update_status = 'UPDATE node SET status=? WHERE point_x=? AND point_y=?'
                c.execute(update_status, (1, canvas.coords(x).pop(0) + 10, canvas.coords(x).pop(1) + 10))


        c.execute('SELECT * FROM node')
        ans = c.fetchall()
        for x in ans:
            print(x)
        print('')

    def handleDeleteButton(self):
        with sqlite3.connect('quit.db') as db:
            # create cursor
            c = db.cursor()

        if len(arr) != 0:
            canvas.delete(location)

            for x in arr_point:
                if (lon >= canvas.coords(x).pop(0) and lon <= canvas.coords(x).pop(2) and
                        lat >= canvas.coords(x).pop(1) and lat <= canvas.coords(x).pop(3)):

                    arr_point.remove(x)

                    delete = "DELETE FROM node WHERE point_x = ? AND point_y = ?"
                    c.execute(delete, (canvas.coords(x).pop(0) + 10, canvas.coords(x).pop(1) + 10))
                    db.commit()

                    canvas.delete(x)  # xóa hình khỏi canvas

                    c.execute('SELECT * FROM node')
                    ans = c.fetchall()
                    for x in ans:
                        print(x)
                    print('')


root = tk.Tk()
ser = serial.Serial("/dev/ttyS0", 9600)
app = MainFrame(root)
root.mainloop()
