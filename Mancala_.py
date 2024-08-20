class Mancala:
    def __init__(self):
        self.Start()
    
    def Start(self):
        print("START")
        self.Setup()
        self.Select()
    
    def Setup(self):
        print('SETUP')

        # board
        #          [4,4,4,4,4,4] player
        # computer [4,4,4,4,4,4]
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        
        # global variables
        self.turn = 'computer'
        self.computerGoal = 0
        self.playerGoal = 0
        self.makeDeeperTree = False
        self.memory = {}
        self.memory_index = 0

        # show board before game start
        self.Display()

    def Select(self):
        print("\n==================== TURN: "+self.turn.upper()+" ====================")

        # player turn
        if self.turn == 'player':
            col = int(input("PLAYER SELECT COL 0-5 >"))
            selected_cell = [1,col]
            if self.board[1][col] > 0:
                self.Move(selected_cell, False)
            else:
                self.Select("[X] Can't select an empty cell")
        
        # computer turn
        elif self.turn == 'computer':
            self.Calculate()

    def Calculate(self):
        print("CALCULATE")
        self.Save()
        for i in range(5):
            self.Load()
        """
        for i in range(5): # first try all 6 options to make a decision tree
            self.computerGoal = tmpCompGoal # go back to the goal that was before
            for row in range(2): # go back to the board that was before
                for col in range(6):
                    self.board[row][col] = tmpBoard[row][col]
            print("* calculating for cell",i)
            if self.board[0][i] > 0: # if this cell is not empty
                self.Move([0,i], True)
                if not self.makeDeeperTree:
                    print("* this tree gives",self.computerGoal,"points")
                else:
                    print("* this tree has another level")
                    self.makeDeeperTree = False
                    self.Calculate()
            else:
                print("* this cell is empty")
        """
    
    def Save(self):
        print("SAVING BOARD")
        print("* memory index",self.memory_index)
        print("* computer goal",self.computerGoal)
        tmpBoard = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for row in range(2):
            for col in range(6):
                tmpBoard[row][col] = self.board[row][col]
        print("* board configuration",tmpBoard)
        tmpGoal = self.computerGoal
        self.memory[self.memory_index] = (tmpBoard, tmpGoal)
        self.memory_index += 1
    
    def Load(self):
        tmp = self.memory[self.memory_index-1]
        for row in range(2):
            for col in range(6):
                self.board[row][col] = self.memory[][row][col]

    def Move(self, selected_cell, simulation):
        go_again = True
        row = selected_cell[0]
        col = selected_cell[1]
        while go_again:
            go_again = False
            print("\nPICK FROM: "+str(row)+","+str(col))

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
        print("DISPLAY")
        print(self.board[0])
        print(self.board[1])
        print('Player Goal = ',self.playerGoal)
        print('Computer Goal = ',self.computerGoal)

Mancala()