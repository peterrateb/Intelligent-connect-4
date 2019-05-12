import numpy as np
'''
Evaluation Table is table contains numbers
    Each number indicates the number of four connected positions
For Example :
    Number 3 in the lower left most corner
    There are 3 wining states which are 
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0.]          ## State 1
        [1. 0. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]          ## State 2
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [1. 1. 1. 1. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]          ## State 3
        [0. 0. 1. 0. 0. 0. 0.]
        [0. 1. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0.]
        
    Number 7 in the Middle of the board
    There are 7 wining states which are 

        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]          ## State 1
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 1. 1. 1. 1.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 1.]          ## State 2
        [0. 0. 0. 0. 0. 1. 0.]
        [0. 0. 0. 0. 1. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]          ## State 3
        [0. 0. 0. 1. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0.]          ## State 4
        [0. 1. 0. 0. 0. 0. 0.]
        [0. 0. 1. 0. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]          ## State 5
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [1. 1. 1. 1. 0. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]          ## State 6
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 1. 1. 1. 1. 0. 0.]
        ----------------------
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]          ## State 7
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 1. 1. 1. 1. 0.]
        ----------------------
       
'''
evaluationTable = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3]
]

class Connect4:
    NOROWS=6
    NOCOLS=7

    def __init__(self):
        self.board=np.zeros((Connect4.NOROWS,Connect4.NOCOLS))
        self.turn=1

    def print_board(self):
        """
        \033[0;37;48m white text
        \033[0;31;48m red text
        \033[0;34;48m blue text
        """
        for row in self.board:
            print("\033[0;37;48m|",end="")
            for cell in row:
                print("\033[0;31;48mO" if cell == 2 else "\033[0;34;48mO" if cell == 1 else "\033[0;37;48m ",end="")
                print("\033[0;37;48m|",end="")
            print("")
            print("\033[0;37;48m---------------")

    def is_valid_place(self,row_no,col_no):
        return (row_no == 6 or self.board[row_no+1] != 0) and self.board[row_no][col_no] == 0

    def detect_valid_first_row(self,col_no):
        if col_no>6 or col_no<0 : return -1
        for i in range(self.NOROWS):
            if self.board[Connect4.NOROWS-i-1][col_no] == 0.0:
                return Connect4.NOROWS-i-1
        return -1

    def add_disk(self,row_no,col_no):
        self.board[row_no][col_no]=self.turn

    def is_any_place_empty(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return True
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def play(self,col_no):
        row_no=self.detect_valid_first_row(col_no)
        if row_no==-1:
            return False
        self.add_disk(row_no,col_no)
        return True
    def check_winner(self):
        #check winner horizontal
        for i in range(Connect4.NOROWS - 3):
            for j in range(Connect4.NOCOLS):
                if self.board[i][j] == self.turn and self.board[i + 1][j] == self.turn and self.board[i + 2][
                    j] == self.turn and self.board[i + 3][j] == self.turn:
                    return True

        #check winner vertical
        for i in range(Connect4.NOROWS):
            for j in range(Connect4.NOCOLS - 3):
                if self.board[i][j] == self.turn and self.board[i][j + 1] == self.turn and self.board[i][
                    j + 2] == self.turn and self.board[i][j + 3] == self.turn:
                    return True

        #check winner positive cross
        for i in range(Connect4.NOROWS - 3):
            for j in range(Connect4.NOCOLS - 3):
                if self.board[i][j] == self.turn and self.board[i + 1][j + 1] == self.turn and self.board[i + 2][
                    j + 2] == self.turn and self.board[i + 3][j + 3] == self.turn:
                    return True

        #check winner negative cross
        for i in range(3, Connect4.NOROWS):
            for j in range(Connect4.NOCOLS - 3):
                if self.board[i][j] == self.turn and self.board[i - 1][j + 1] == self.turn and self.board[i - 2][
                    j + 2] == self.turn and self.board[i - 3][j + 3] == self.turn:
                    return True
        return False
    def game(self):
        #need to check if int and time count
        self.print_board()
        while self.is_any_place_empty():
            print("player " + str(self.turn) + " has evaluation of " + str(self.evaluate()) )
            col_no = input("player" + str(self.turn) + " turn, please enter a column number")

            while not(self.play(int(col_no))):
                col_no = input("player" + str(self.turn) + " turn, Invalid disk location please enter a valid column number")
            self.print_board()
            if self.check_winner()==True:
                print("player"+str(self.turn)+" is the winner")
                exit()
            self.change_turn()
        if self.check_winner() == True:
            print("player" + str(self.turn) + " is the winner")
        else:
            print("No one win")
    def evaluate(self):
        # utility value is the sum of all evaluationTable elements
        sum = 0
        if(self.turn==1):
            for i in range(6):
                for j in range(7):
                    if (self.board[i][j]== 1):
                        sum += evaluationTable[i][j]
                    elif (self.board[i][j] == 2):
                        sum -= evaluationTable[i][j]
        else:
            for i in range(6):
                for j in range(7):
                    if (self.board[i][j]== 2):
                        sum += evaluationTable[i][j]
                    elif (self.board[i][j] == 1):
                        sum -= evaluationTable[i][j]
        #print(self.turn)
        #print(self.board)
        return sum




x=Connect4()
x.game()
