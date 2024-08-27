import tkinter
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import random

class GUI:
    def __init__(self):
        # global variables
        self.images = {}
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        #self.board = [[13,0,3,4,5,6],[7,8,9,10,11,12]]
        self.computerGoal = 0
        self.playerGoal = 0
        self.cells = [[],[]]

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
        self.moving_animation_length = 1000
        self.moving_animation_top = -100

        # setup canvas
        self.canvas = Canvas(self.root, width=self.W, height=self.H, bg="black")
        self.canvas.grid(row=0, column=0)

        # load images
        for path, directories, files in os.walk('images'):
            for file in files:
                if ".png" in file:
                    transpose_one = False
                    if "-goal-no-background" in file:
                        transpose_one = True
                    resize = not "-single-marble-no-background" in file
                    original_size = "button.png" in file
                    path = path.replace("\\","/")
                    self.LoadImage(path+"/"+file, transpose_one, resize, original_size)
        # create objects
        obj_board = self.canvas.create_image(0, 0, image=self.images["images/clean"], anchor=NW)
        
        # cells
        row = 0
        col = 0
        for i in range(12):
            col = i % 6
            if i > 5:
                row = 1
            vadjust = 0
            hadjust = 0
            if col == 0 and row == 1:
                hadjust = -10
            if col == 4 and row == 1:
                hadjust = 5
            if col == 5 and row == 1:
                hadjust = 13
                vadjust = -2
                
            cell_img = self.GetCellImg(row,col)
            obj_cell = self.canvas.create_image((-200+col*103)+hadjust, (-100+(row*100))+vadjust, image=cell_img, anchor=NW)
            self.cells[row].append(obj_cell)

        # goals
        # computer goal
        pcg_img = self.GetGoalImg('computer')
        self.obj_computer_goal = self.canvas.create_image(0, 0, image=pcg_img, anchor=NW)
        # player goal
        plg_img = self.GetGoalImg('player')
        self.obj_player_goal = self.canvas.create_image(-13, -10, image=plg_img, anchor=NW)

        # sigle stone
        single_stone_img = self.GetSingleStoneImg()
        self.obj_single_stone = self.canvas.create_image(-500, -500, image=single_stone_img, anchor=NW)

        # select cell buttons
        for col in range(6):
            x1 = 170+col*105
            y1 = 270
            #x2 = x1+80
            #y2 = y1+70
            tag_name = "btn"+str(col)
            #obj_button = self.canvas.create_oval(x1,y1,x2,y2,fill='red',tag=tag_name)
            btn_img = self.images["images/buttons/button"]
            self.canvas.create_image(x1, y1, image=btn_img, anchor=NW, tag=tag_name)
            self.canvas.tag_bind(tag_name, "<Enter>", lambda event: self.check_hand_enter())
            self.canvas.tag_bind(tag_name, "<Leave>", lambda event: self.check_hand_leave())
            self.canvas.tag_bind(tag_name, "<Button-1>", lambda event: self.click(self))
            #self.canvas.itemconfigure(tag_name, state='hidden')

        # run main loop
        self.root.mainloop()
        
    def AnimationPutToCell(self, row, col, top):
        go_again = False
        end = 160+row*103
        if top == self.moving_animation_top:
            go_again = True
            self.UpdateSprite(self.obj_single_stone, self.GetSingleStoneImg())
            self.canvas.coords(self.obj_single_stone, 200+col*100, top)

        if top < end:
            go_again = True
            self.canvas.move(self.obj_single_stone, 0, 2)
            top += 2
        else:
            # animation over
            print("animation over")
            self.AddToCell(row, col, 1)
            self.canvas.coords(self.obj_single_stone, -500, -500)
        
        if go_again:
            self.root.after(1, lambda:self.AnimationPutToCell(row, col, top))

    def AnimationPutToGoal(self, goal, top):
        go_again = False
        end = 250
        if goal == "computer":
            x = 80
        else:
            x = 800
        
        if top == self.moving_animation_top:
            go_again = True
            self.UpdateSprite(self.obj_single_stone, self.GetSingleStoneImg())
            self.canvas.coords(self.obj_single_stone, x, top)

        if top < end:
            go_again = True
            self.canvas.move(self.obj_single_stone, 0, 2)
            top += 2
        else:
            # animation over
            print("animation over")
            self.AddToGoal(goal, 1)
            self.canvas.coords(self.obj_single_stone, -500, -500)
        
        if go_again:
            self.root.after(1, lambda:self.AnimationPutToGoal(goal, top))

    def AnimationTakeFromCell(self, row, col, num, end):
        go_again = False
        if end == self.moving_animation_length:
            self.AddToCell(row, col, -1)
            self.UpdateSprite(self.obj_single_stone, self.GetSingleStoneImg())
            self.canvas.coords(self.obj_single_stone, 200+col*100, 160+row*103)
            go_again = True
        if end > 0:
            end -= 1
            self.canvas.move(self.obj_single_stone, 0, -2)
            go_again = True
        elif end == 0:
            end = self.moving_animation_length
            if num > 1:
                num -= 1
                go_again = True
        
        if go_again:
            self.root.after(1, lambda:self.AnimationTakeFromCell(row, col, num, end))
        else:
            # animation over
            print("animation over")


    def AnimationTakeFromGoal(self, goal, num, end):
        go_again = False
        if end == self.moving_animation_length:
            self.AddToGoal(goal, -1)
            self.UpdateSprite(self.obj_single_stone, self.GetSingleStoneImg())
            if goal == "computer":
                self.canvas.coords(self.obj_single_stone, 100, 250)
            else:
                self.canvas.coords(self.obj_single_stone, 800, 250)
            go_again = True
        if end > 0:
            end -= 1
            self.canvas.move(self.obj_single_stone, 0, -2)
            go_again = True
        elif end == 0:
            end = self.moving_animation_length
            if num > 1:
                num -= 1
                go_again = True
        
        if go_again:
            self.root.after(1, lambda:self.AnimationTakeFromGoal(goal, num, end))
        else:
            # animation over
            print("animation over")

    def AddToGoal(self, pcpl, num):
        if pcpl == "computer":
            self.computerGoal += num
            self.UpdateSprite(self.obj_computer_goal, self.GetGoalImg('computer'))
        else:
            self.playerGoal += num
            self.UpdateSprite(self.obj_player_goal, self.GetGoalImg('player'))

    def AddToCell(self, row, col, num):
        self.board[row][col] += num
        self.UpdateSprite(self.cells[row][col], self.GetCellImg(row, col))

    def LoadImage(self, filename, transpose_one, resize, original_size):
        image = Image.open(filename)
        if not original_size:
            if resize:
                image = image.resize((self.W,self.H), Image.LANCZOS)
            else:
                image = image.resize((int(111/2),int(114/2)), Image.LANCZOS)
        photoimage = ImageTk.PhotoImage(image)
        self.images[filename.replace(".png", "")] = photoimage
        if transpose_one:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            photoimage = ImageTk.PhotoImage(image)
            self.images[filename.replace(".png", "-transposed")] = photoimage
    
    def GetCellImg(self, row, col):
        number_of_stones = self.board[row][col]
        if number_of_stones > 13:
            number_of_stones = 13
        return self.images["images/cells/"+str(number_of_stones).zfill(2)+"-single-cell-no-background"]
    
    def GetGoalImg(self, pcpl):
        transpose = ""
        if pcpl == "computer":
            number_of_stones = self.computerGoal
        else:
            number_of_stones = self.playerGoal
            transpose = "-transposed"
        return self.images["images/goals/"+str(number_of_stones).zfill(2)+"-goal-no-background"+transpose]
    
    def GetSingleStoneImg(self):
        color = random.randint(1,5)
        return self.images["images/stones/"+str(color).zfill(2)+"-single-marble-no-background"]

    def UpdateSprite(self, Object, Sprite):
        self.canvas.itemconfig(Object, image = Sprite)

    def check_hand_enter(self):
        self.canvas.config(cursor="hand2")

    def check_hand_leave(self):
        self.canvas.config(cursor="")

    def click(event, self):
        button = self.canvas.gettags("current")[0] # string type with values: btn0, btn1 .. btn5

    def exit(self):
        self.root.destroy()
        os._exit(1)


GUI()