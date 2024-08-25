import tkinter
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk, Image
from tkinter import filedialog
import os

class GUI:    
    def SetupGUI(self):
        # setup main window
        self.root = tkinter.Tk()
        self.W = int(1920/2)
        self.H = int(1080/2)
        self.root.geometry(str(self.W)+"x"+str(self.H))
        self.root.minsize(self.W,self.H)
        self.root.title("Sudoku Solver v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # setup canvas
        self.canvas = Canvas(self.root, width=self.W, height=self.H, bg="black")
        self.canvas.grid(row=0, column=0)
    
    def DrawBoard(self):
        print("its alive")
        # draw board
        image_path = "clean.png"
        image = Image.open(image_path)
        image = image.resize((self.W,self.H), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=photo)
    
    def MainLoop(self):
        print("mainloop")
        self.root.mainloop()
    
    def exit(self):
        self.root.destroy()
        os._exit(1)