import sys

class Node:
    def __init__(self):
        self.board = [[4,4,4,4,4,4],[4,4,4,4,4,4]] # this is the board before move
        self.score = 0
        self.next = [None,None,None,None,None,None]
        self.prev = None
        self.name = 0

class Functions:    
    def __init__(self):
        print('SETUP')

        # board
        #          [4,4,4,4,4,4] player
        # computer [4,4,4,4,4,4]
        self.starting_with = 4
        self.board = [[self.starting_with,self.starting_with,self.starting_with,self.starting_with,self.starting_with,self.starting_with],[self.starting_with,self.starting_with,self.starting_with,self.starting_with,self.starting_with,self.starting_with]]
        #self.board = [[0,0,0,0,0,0],[3,3,3,3,3,3]]
        #self.board = [[2,2,2,2,2,2],[2,2,2,2,2,2]]
        #self.board = [[1,1,1,1,1,1],[1,1,1,1,1,1]]
        
        # global variables
        self.turn = 'Player'
        self.computerGoal = 0
        self.playerGoal = 0
        self.makeDeeperTree = False
        self.pointer = Node()
        self.nodeName = 0
        self.max_score = 0
        self.max_score_path = []
        self.animations = []
        self.game_over = False
        self.status = ""

        # show board before game start
        self.Display()
    
    def Select(self, col):
        print("SELECT")
        print("WAITING FOR INPUT FROM: "+self.turn.upper())
        # player turn
        if not self.game_over:
            if self.turn == 'Player':
                selected_cell = [1,col]
                print("SELECTED CELL >"+str(selected_cell[1]))
                self.Move(selected_cell, False)
            elif self.turn == 'Computer':
                if len(self.max_score_path) == 0:
                    self.makeDeeperTree = False
                    self.pointer = Node()
                    self.nodeName = 0
                    self.max_score = 0
                    self.max_score_path = []
                    # save a copy of the board
                    self.Save()
                    self.Calculate()
                
                if len(self.max_score_path) > 0:
                    selected_cell = [0,self.max_score_path.pop()]
                else:
                    col = 0
                    while self.board[0][col] == 0:
                        col += 1
                    selected_cell = [0,col]
                #print("[>] Computer select cell 0-5 >",selected_cell[1])
                self.Move(selected_cell, False)

        """
        ##print("Select:")
        #print("Waiting for input from:",self.turn)

        # player turn
        if self.turn == 'Player':
            col = -1
            while not col in (0,1,2,3,4,5):
                try:
                    col = int(input("[>] Player select cell 0-5 >"))
                except:
                    col = -1
            selected_cell = [1,col]
            if self.board[1][col] > 0:
                self.Move(selected_cell, False)
            else:
                ##print("[X] Can't select an empty cell")
                self.Select()
        
        # computer turn
        elif self.turn == 'Computer':
            if len(self.max_score_path) == 0:
                self.makeDeeperTree = False
                self.pointer = Node()
                self.nodeName = 0
                self.max_score = 0
                self.max_score_path = []
                # save a copy of the board
                self.Save()
                self.Calculate()
            
            if len(self.max_score_path) > 0:
                selected_cell = [0,self.max_score_path.pop()]
            else:
                col = 0
                while self.board[0][col] == 0:
                    col += 1
                selected_cell = [0,col]
            ##print("[>] Computer select cell 0-5 >",selected_cell[1])
            self.Move(selected_cell, False)
        """

    def Calculate(self):
        print("CALCULATING...")
        goAgain = True
        cell = 0
        steps = 0
        self.simulation = True

        while goAgain:
            steps += 1
            #input("Continue #"+str(steps)+" >")
            goAgain = False
            if cell < 6:
                ##print("Board before move:",self.board)
                ##print("[>] Computer select cell 0-5 >",cell)
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
                        ##print("[!] This tree gives",self.computerGoal,"points")
                        self.GoUp()
                        self.Load()
                    else:
                        ##print("[!] This tree has another level")
                        goAgain = True
                        cell = 0
                        self.makeDeeperTree = False
                else:
                    ##print("[X] this cell is empty")
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
                        ##print("will go to",i,"next")
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
                            ##print("Max score:",self.max_score)
                            #self.max_score_path = list(reversed(self.max_score_path))
                            ##print("Path to max score:",self.max_score_path)
                self.Load()
        print("DONE")

    def Save(self):
        ###print("Save:")
        
        # save a copy of the board
        tmpBoard = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
        for row in range(2):
            for col in range(6):
                tmpBoard[row][col] = self.board[row][col]
        
        # save a copy of the goal
        tmpGoal = self.computerGoal

        # display for user
        ##print("#"+str(self.nodeName),tmpBoard,"$"+str(tmpGoal))

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
            ##print("New max score:",self.max_score)
            ##print("Path:",self.max_score_path)

    def Load(self):
        ###print("Load:")

        # load a copy of the board
        for row in range(2):
            for col in range(6):
                self.board[row][col] = self.pointer.board[row][col]
        
        # load a copy of the goal
        self.computerGoal = self.pointer.score

        # display for user
        ##print("#"+str(self.pointer.name),self.board,"$"+str(self.computerGoal))

    def GoUp(self):
        if self.pointer.prev != None:
            tmp = self.pointer
            self.pointer = tmp.prev
            ##print("Go up to ->",self.pointer.name)
        else:
            return 1

    def Move(self, selected_cell, simulation):
        if not self.game_over:
            go_again = True
            row = selected_cell[0]
            col = selected_cell[1]
            while go_again:
                go_again = False
                if not simulation:
                    print("PICK FROM >"+str(row)+","+str(col))
                    pass

                # take all the stones from the selected cell to hand
                hand = self.board[row][col]
                self.board[row][col] = 0
                if not simulation:
                    self.AddToAnimationList("AnimationTakeFromCell", row, col, self.turn, hand)

                # circle while there are stones in hand
                while hand > 0:
                    if row == 1: # if pointer is on the players side
                        if col < 5: # didn't reach the goal yet
                            col += 1 # point to the next selcted cells
                            hand -= 1
                            self.board[row][col] += 1 # put one stone down from hand to next cell
                            if not simulation:
                                self.AddToAnimationList("AnimationPutToCell", row, col, self.turn, 1)
                        elif col == 5:
                            col = 6
                            row = 0 # switch to row computer
                            if self.turn == 'Player':
                                hand -= 1
                                self.playerGoal += 1
                                if not simulation:
                                    self.AddToAnimationList("AnimationPutToGoal", row, col, self.turn, 1)
                    
                    elif row == 0: # if pointer is on the computer side
                        if col > 0: # didn't reach the goal yet
                            col -= 1 # point to the next selcted cells
                            hand -= 1
                            self.board[row][col] += 1 # put one stone down from hand to next cell
                            if not simulation:
                                self.AddToAnimationList("AnimationPutToCell", row, col, self.turn, 1)
                        elif col == 0:
                            col = -1
                            row = 1 # switch to row player
                            if self.turn == 'Computer':
                                hand -= 1
                                self.computerGoal += 1
                                if not simulation:
                                    self.AddToAnimationList("AnimationPutToGoal", row, col, self.turn, 1)
                if not simulation:
                    self.Display()

                # end
                if col != -1 and col != 6:
                    if self.board[row][col] > 1: # if we landed on a not empty cell then
                        go_again = True
            
            if not simulation:
                switch_turn = True
                if self.turn == 'Player' and col == 6: # player select again
                    switch_turn = False
                if self.turn == 'Computer' and col == -1: # player select again
                    switch_turn = False

                if switch_turn:
                    if self.turn == 'Player':
                        self.turn = 'Computer'
                    else:
                        self.turn ='Player'
                
                # winner test
                self.game_over = False
                winning_sum = (self.starting_with*12)/2
                if self.computerGoal > winning_sum:
                    self.status = "Computer won the game!"
                    self.game_over = True

                if self.playerGoal > winning_sum:
                    self.status = "Player won the game!"
                    self.game_over = True

                if self.playerGoal == winning_sum and self.computerGoal == winning_sum:
                    self.status = "Its a draw!"
                    self.game_over = True
                
                # paralized test
                computerParalized = True
                playerParalized = True
                for i in self.board[0]:
                    if i > 0:
                        computerParalized = False
                for i in self.board[1]:
                    if i > 0:
                        playerParalized = False
                
                if computerParalized and self.turn == 'Computer':
                    self.turn = 'Player'
                
                if playerParalized and self.turn == 'Player':
                    self.turn = 'Computer'

                if computerParalized and playerParalized:
                    if self.playerGoal > self.computerGoal:
                        self.status = "Player won the game!"
                        pass
                    elif self.playerGoal < self.computerGoal:
                        self.status = "Computer won the game!"
                        pass
                    elif self.playerGoal == self.computerGoal:
                        self.status = "Its a draw!"
                        pass
                    self.game_over = True

                # play again
                if self.game_over:
                    print("GAME OVER")
                    pass

            else:
                if self.turn == 'Computer' and col == -1: # continue the tree deeper
                    self.makeDeeperTree = True

    def Display(self):
        #print("Display:")
        print(self.board[0])
        print(self.board[1])
        print('PL $'+str(self.playerGoal))
        print('PC $'+str(self.computerGoal))
        pass
    
    def AddToAnimationList(self, next_animation, row, col, goal, num):
        self.animations.append((next_animation, row, col, goal, num))