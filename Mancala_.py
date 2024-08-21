class Mancala:
    def __init__(self):
        self.Start()
    
    def Start(self):
        print("\nStart:")
        self.Setup()
        self.Select()
    
    def Setup(self):
        print('\nSetup:')

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
        print("\nSelect:")
        print("Waiting for input from:",self.turn)

        # player turn
        if self.turn == 'player':
            col = int(input("[>] Player select cell 0-5 >"))
            selected_cell = [1,col]
            if self.board[1][col] > 0:
                self.Move(selected_cell, False)
            else:
                self.Select("[X] Can't select an empty cell")
        
        # computer turn
        elif self.turn == 'computer':
            self.Calculate(0)

    def Calculate(self, tree_lvl):
        print("\nCalculate:")
        print("Calculate for tree lvl:",tree_lvl)
        self.Save()
        for cell in range(5):
            print("Running for cell",cell,"tree lvl:",tree_lvl)
            if self.board[0][cell] > 0:
                self.Load()
                self.Move([0,cell], True)
                if not self.makeDeeperTree:
                    print("[!] This tree gives",self.computerGoal,"points")
                else:
                    print("[!] This tree has another level")
                    self.makeDeeperTree = False
                    self.Calculate(tree_lvl+1)
            else:
                print("[X] this cell is empty")
    
    def Save(self):
        print("\nSave:")
        print("memory index",self.memory_index)
        print("computer goal",self.computerGoal)
        tmpBoard = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for row in range(2):
            for col in range(6):
                tmpBoard[row][col] = self.board[row][col]
        print("board configuration",tmpBoard)
        tmpGoal = self.computerGoal
        self.memory[self.memory_index] = (tmpBoard, tmpGoal)
        self.memory_index += 1
    
    def Load(self):
        print("\nLoad:")
        print("memory index",self.memory_index-1)
        print("computer goal",self.computerGoal)
        tmp = self.memory[self.memory_index-1]
        for row in range(2):
            for col in range(6):
                self.board[row][col] = tmp[0][row][col]
        print("board configuration",self.board)

    def Move(self, selected_cell, simulation):
        print("\nMove:")
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
        print("\nDisplay:")
        print(self.board[0])
        print(self.board[1])
        print('Player Goal = ',self.playerGoal)
        print('Computer Goal = ',self.computerGoal)

Mancala()
