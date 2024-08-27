import tkinter
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk, Image
from tkinter import filedialog
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
        self.root.minsize(W,H)
        self.root.title("Sudoku Solver v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.image_path = "clean.png"
        image = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(image)
        self.label = Label(self.root, image=photo)
        self.label.pack(fill=BOTH, expand=YES)
        self.root.bind('<Configure>', self.resize_image)


        """
        # load board
        image_path = "clean.png"  # Replace with your image path
        image = Image.open(image_path)
        image = image.resize((W,H), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        canvas = Canvas(self.root, width=W, height=H, bg="black")
        canvas.pack(fill=BOTH, expand=YES)
        canvas.create_image(0, 0, anchor=NW, image=photo)
        """

        # Run the Tkinter event loop
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        os._exit(1)
    
    def resize_image(self, event):
        # Resize the image to fit the new window size, maintaining aspect ratio
        new_width = event.width
        new_height = event.height

        # Open the image file again and resize it
        image = Image.open(self.image_path)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        # Update the PhotoImage object
        self.photo = ImageTk.PhotoImage(resized_image)
        self.label.config(image=self.photo)
        self.label.image = self.photo  # Prevent garbage collection

GUI()