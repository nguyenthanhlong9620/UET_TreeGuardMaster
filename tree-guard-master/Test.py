from tkinter import *
from tkinter import messagebox as ms
import tkinter as tk
from tkinter import font as tkfont

from pip._vendor.cachecontrol import controller

from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


def event2canvas(e, c): return (c.canvasx(e.x), c.canvasy(e.y))


class MapApp(tk.Tk):

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
        for F in (StartPage,):
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
        # setting up a tkinter canvas with scrollbars
        frame = Frame(tk, bd=2, relief=SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        xscroll = Scrollbar(frame, orient=HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky=E+W)
        yscroll = Scrollbar(frame)
        yscroll.grid(row=0, column=1, sticky=N+S)
        canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set,
                        yscrollcommand=yscroll.set)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        xscroll.config(command=canvas.xview)
        yscroll.config(command=canvas.yview)
        frame.pack(fill=BOTH, expand=1)

        # adding the image
        File = askopenfilename(parent=tk, initialdir="M:/",
                               title='Choose an image.')
        print("opening %s" % File)
        # img = PhotoImage(file=File)

        img = ImageTk.PhotoImage(Image.open(File))  # PIL solution

        canvas.create_image(0, 0, image=img, anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))

        def printcoords(event):
            # outputting x and y coords to console
            cx, cy = event2canvas(event, canvas)
            print("(%d, %d) / (%d, %d)" % (event.x, event.y, cx, cy))
        # mouseclick event
        canvas.bind("<ButtonPress-1>", printcoords)
        canvas.bind("<ButtonRelease-1>", printcoords)


if __name__ == "__main__":
    app = MapApp()
    app.mainloop()
