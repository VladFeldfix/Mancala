import tkinter
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk, Image
from tkinter import filedialog
import os

class GUI:
    def __init__(self):
        # global variables
        self.images = {}
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        self.cells = []

        # run
        self.SetupGUI()

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

        # load images
        for path, directories, files in os.walk('images'):
            for file in files:
                if ".png" in file:
                    self.LoadImage("images/"+file)
        
        # create objects
        obj_board = self.canvas.create_image(0, 0, image=self.images["clean"], anchor=NW)
        # cell buttons
        row = 0
        col = 0
        for i in range(12):
            col = i % 6
            if i > 5:
                row = 1
            obj_cell = self.canvas.create_image(-200+col*103, -100+(row*100), image=self.images["13-single-cell-no-background"], anchor=NW)
            self.cells.append(obj_cell)

        # run main loop
        self.root.mainloop()

    def LoadImage(self, filename):
        image = Image.open(filename)
        image = image.resize((self.W,self.H), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        self.images[filename.replace("images/", "").replace(".png", "")] = image

    def UpdateSprite(self, Object, Sprite):
        self.canvas.itemconfig(Object, image = Sprite)

    def exit(self):
        self.root.destroy()
        os._exit(1)


GUI()