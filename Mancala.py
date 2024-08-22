import sys
class Node:
    def __init__(self):
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]] # this is the board before move
        self.score = 0
        self.next = [None,None,None,None,None,None]
        self.prev = None
        self.name = 0

class Mancala:
    def __init__(self):
        self.Start()
    
    def Start(self):
        print("\nStart")
        self.Setup()
        self.Select()
    
    def Setup(self):
        #print('\nSetup:')

        # board
        #          [4,4,4,4,4,4] player
        # computer [4,4,4,4,4,4]
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        #self.board = [[3,3,3,3,3,3],[3,3,3,3,3,3]]
        #self.board = [[2,2,2,2,2,2],[2,2,2,2,2,2]]
        #self.board = [[1,1,1,1,1,1],[1,1,1,1,1,1]]
        
        # global variables
        self.turn = 'computer'
        self.computerGoal = 0
        self.playerGoal = 0
        self.makeDeeperTree = False
        self.pointer = Node()
        self.nodeName = 0
        self.max_score = 0
        self.max_score_path = []

        # show board before game start
        self.Display()
    
    def Select(self):
        #print("\nSelect:")
        #print("Waiting for input from:",self.turn)

        # player turn
        if self.turn == 'player':
            col = int(input("[>] Player select cell 0-5 >"))
            selected_cell = [1,col]
            if self.board[1][col] > 0:
                self.Move(selected_cell, False)
            else:
                print("[X] Can't select an empty cell")
                self.Select()
        
        # computer turn
        elif self.turn == 'computer':
            # save a copy of the board
            self.Save()
            self.Calculate()
    
    def Calculate(self):
        print("\nCalculate:")
        goAgain = True
        cell = 0
        steps = 0
        self.simulation = True

        while goAgain:
            steps += 1
            print("Continue #"+str(steps)+" >")
            goAgain = False
            if cell < 6:
                print("Board before move:",self.board)
                print("[>] Computer select cell 0-5 >",cell)
                if self.board[0][cell] > 0:
                    self.Move([0,cell], True)
                    self.pointer.next[cell] = Node()
                    tmp = self.pointer
                    self.pointer = self.pointer.next[cell]
                    self.pointer.prev = tmp
                    self.Save()
                    if not self.makeDeeperTree:
                        goAgain = True
                        cell += 1
                        print("[!] This tree gives",self.computerGoal,"points")
                        self.GoUp()
                        self.Load()
                    else:
                        print("[!] This tree has another level")
                        goAgain = True
                        cell = 0
                        self.makeDeeperTree = False
                else:
                    print("[X] this cell is empty")
                    self.pointer.next[cell] = "Empty"
                    cell += 1
                    goAgain = True
            else:
                # going up a level back to where it was
                self.GoUp()
                i = 0
                tmp = 0
                while tmp != None:
                    if i < 6:
                        tmp = self.pointer.next[i]
                        print("will go to",i,"next")
                        cell = i
                        i += 1
                        goAgain = True
                    else:
                        goupresult = self.GoUp()
                        i = 0
                        cell = i
                        if goupresult == None:
                            goAgain = True
                        else:
                            tmp = None
                            goAgain = False
                            print("Max score:",self.max_score)
                            self.max_score_path = list(reversed(self.max_score_path))
                            print("Path to max score:",self.max_score_path)
                self.Load()


    def Save(self):
        print("\nSave:")
        
        # save a copy of the board
        tmpBoard = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for row in range(2):
            for col in range(6):
                tmpBoard[row][col] = self.board[row][col]
        
        # save a copy of the goal
        tmpGoal = self.computerGoal

        # display for user
        print("#"+str(self.nodeName),tmpBoard,"$"+str(tmpGoal))

        # save to database
        self.pointer.board = tmpBoard
        self.pointer.score = tmpGoal
        self.pointer.name = self.nodeName
        self.nodeName += 1
        if self.pointer.score > self.max_score:
            self.max_score = self.pointer.score
            tmpointer = self.pointer
            self.max_score_path = []
            while tmpointer.prev != None:
                inx = tmpointer.prev.next.index(tmpointer)
                self.max_score_path.append(inx)
                tmpointer = tmpointer.prev

    def Load(self):
        print("\nLoad:")

        # load a copy of the board
        for row in range(2):
            for col in range(6):
                self.board[row][col] = self.pointer.board[row][col]
        
        # load a copy of the goal
        self.computerGoal = self.pointer.score

        # display for user
        print("#"+str(self.pointer.name),self.board,"$"+str(self.computerGoal))

    def GoUp(self):
        if self.pointer.prev != None:
            tmp = self.pointer
            self.pointer = tmp.prev
            print("Go up to ->",self.pointer.name)
        else:
            return 1

    def Move(self, selected_cell, simulation):
        #print("\nMove:")
        go_again = True
        row = selected_cell[0]
        col = selected_cell[1]
        while go_again:
            go_again = False
            print("Pick from: "+str(row)+","+str(col))

            # take all the stones from the selected cell to hand
            hand = self.board[row][col]
            self.board[row][col] = 0

            # circle while there are stones in hand
            while hand > 0:
                if row == 1: # if pointer is on the players side
                    if col < 5: # didn't reach the goal yet
                        col += 1 # point to the next selcted cells
                        hand -= 1
                        self.board[row][col] += 1 # put one stone down from hand to next cell
                    elif col == 5:
                        col = 6
                        row = 0 # switch to row computer
                        if self.turn == 'player':
                            hand -= 1
                            self.playerGoal += 1
                
                elif row == 0: # if pointer is on the computer side
                    if col > 0: # didn't reach the goal yet
                        col -= 1 # point to the next selcted cells
                        hand -= 1
                        self.board[row][col] += 1 # put one stone down from hand to next cell
                    elif col == 0:
                        col = -1
                        row = 1 # switch to row player
                        if self.turn == 'computer':
                            hand -= 1
                            self.computerGoal += 1
            self.Display()

            # end
            if col != -1 and col != 6:
                if self.board[row][col] > 1: # if we landed on a not empty cell then
                    go_again = True
        
        if not simulation:
            switch_turn = True
            if self.turn == 'player' and col == 6: # player select again
                switch_turn = False

            if switch_turn:
                if self.turn == 'player':
                    self.turn = 'computer'
                else:
                    self.turn ='player'
            
            self.Select()
        else:
            if self.turn == 'computer' and col == -1: # continue the tree deeper
                self.makeDeeperTree = True


    def Display(self):
        #print("\nDisplay:")
        print(self.board[0])
        print(self.board[1])
        print('PL $'+str(self.playerGoal))
        print('PC $'+str(self.computerGoal))

Mancala()