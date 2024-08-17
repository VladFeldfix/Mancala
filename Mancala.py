class Mancala:
    def __init__(self):
        self.Setup()
        self.Select()
    
    def Setup(self):
        #          [4,4,4,4,4,4] player
        # computer [4,4,4,4,4,4]
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
        #self.board = [[0,0,0,0,0,0],[0,0,0,0,0,1]]
        self.computerGoal = 0
        self.playerGoal = 0
        self.turn = 'player'
        self.Display()
    
    def Select(self):
        selected_cell = [1,5]
        self.Move(selected_cell)

    def Move(self, selected_cell): # selected_cell = [0 or 1, 0-7]
        print("\nPICK UP FROM:",selected_cell)
        #  computer [00,01,02,03,04,05] 
        #           [10,11,12,13,14,15] player
        hand = self.board[selected_cell[0]][selected_cell[1]]
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
        if col != -1 and col != 6:
            if self.board[row][col] > 1: # if we landed on a not empty cell then
                self.Move([row,col])
        if self.turn == 'player' and col == 6:
            print("\nSELECTING AGAIN")
            self.Select()

    def Display(self):
        print(self.board[0])
        print(self.board[1])
        print('Player Goal = ',self.playerGoal)
        print('Computer Goal = ',self.computerGoal)
                    
Mancala()