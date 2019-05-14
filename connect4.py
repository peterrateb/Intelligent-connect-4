import numpy as np
import colorama
from colorama import Fore, Back

class Connect4:
    NOROWS=6
    NOCOLS=7

    def __init__(self):
        self.board=np.zeros((Connect4.NOROWS,Connect4.NOCOLS))
        self.turn=1

    def print_board(self):
        print(" 1 2 3 4 5 6 7")
        for row in self.board:
            print("|",end="")
            for cell in row:
                print( Fore.RED + "O" if cell == 2 else Fore.BLUE + "O" if cell == 1 else " ",end="")
                print("|",end="")
            print("")
            print("---------------")


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
        return False
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
    
    def save(self):
        np.savetxt("connect4.txt",self.board,delimiter=' ',fmt='%1.0f')

    def load(self):
        self.board=np.loadtxt("connect4.txt",delimiter=' ')
        
    def game(self):
        #need to check if int and time count
        self.print_board()
        while self.is_any_place_empty():
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
            
if __name__=="__main__":
    colorama.init(autoreset=True)# Automatically adds a Style.RESET_ALL after each print statement
    x=Connect4()
    x.game()
