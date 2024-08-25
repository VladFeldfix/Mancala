import tkinter
from tkinter import *
from tkinter import font as tkfont
import os

class GUI:
    def __init__(self):
        self.setup_gui()
    
    def setup_gui(self):
        # setup main window
        self.root = tkinter.Tk()
        W = int(1920/2)
        H = int(1080/2)
        self.root.geometry(str(W)+"x"+str(H))
        self.root.minsize(363,399)
        self.root.title("Sudoku Solver v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        canvas = Canvas(width=300, height=200, bg='black')


        # run main loop
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        os._exit(1)

GUI()