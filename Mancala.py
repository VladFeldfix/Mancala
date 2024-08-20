class Mancala:
    def __init__(self):
        self.Start()

    def Start(self):
        print("START")
        self.Setup()
        self.Select()
    
    def Setup(self):
        print("SETUP")
        #          [4,4,4,4,4,4] player
        # computer [4,4,4,4,4,4]
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        #self.board = [[0,0,0,0,0,0],[0,0,0,0,0,1]]
        self.computerGoal = 0
        self.playerGoal = 0
        self.turn = 'player'
        self.computerMoves = []
        self.memory = []
        self.Display()
    
    def Select(self):
        print("\n==================== TURN: "+self.turn.upper()+" ====================")
        if self.turn == 'player':
            col = int(input("PLAYER SELECT COL 0-5 >"))
            selected_cell = [1,col]
            self.Move(selected_cell)
        
        if self.turn == 'computer':
            if len(self.computerMoves) == 0:
                self.computerMoves = self.Calculate()
            else:
                nextMove = self.computerMoves.pop()
                print("COMPUTER SELECT COL 0-5 >"+str(nextMove[1]))
                self.Move(nextMove)
        
    def Calculate(self):
        self.SaveBoard()
        for i in range(6):
            print("* Computer calculating for move 0,"+str(i))
        return [[0,0],]

    def Move(self, selected_cell): # selected_cell = [0 or 1, 0-7]
        switch_turn = True
        print("\nPICK FROM:",selected_cell)
        #  computer [00,01,02,03,04,05] 
        #           [10,11,12,13,14,15] player
        hand = self.board[selected_cell[0]][selected_cell[1]]
        if hand == 0:
            print("[X] Can't choose that spot!")
            switch_turn = False

        self.board[selected_cell[0]][selected_cell[1]] = 0 # pick up all the rocks from the selected cell to hand 
        row = selected_cell[0]
        col = selected_cell[1]

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
        if col != -1 and col != 6: # continue going
            if self.board[row][col] > 1: # if we landed on a not empty cell then
                self.Move([row,col])
                switch_turn = False
                go_again = False

        if self.turn == 'player' and col == 6: # player select again
            switch_turn = False
    
        # end of turn
        # change the turn
        if switch_turn:
            if self.turn == 'player':
                self.turn = 'computer'
            else:
                self.turn ='player'
        
        # go
        self.Select()
        return

    def SaveBoard(self):
        print("SAVED BOARD")
        tmp = self.board.copy()
        self.memory.append(tmp)
        print("Memory bank:")
        x = 0
        for i in self.memory:
            x += 1
            print("  ",x,i)

    def Display(self):
        print("DISPLAY")
        print(self.board[0])
        print(self.board[1])
        print('Player Goal = ',self.playerGoal)
        print('Computer Goal = ',self.computerGoal)
                    
Mancala()