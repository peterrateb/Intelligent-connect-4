from connect4 import Connect4
from enum import Enum
class GameMode(Enum):
    AI=0
    NETWORK=1
def startGame(connect4,mode):
    connect4.game()
if __name__=="__main__":
    print("Welcome to Connect 4 game")
    print("Please choose option number.")
    print("1.New Game")
    print("2.Load Game")
    choosenNumber=input()
    choosenNumber=int(choosenNumber)
    connect4 = Connect4()
    if choosenNumber==1:
        print("Please choose option number.")
        print("1.VS Local AI")
        print("2.VS Network AI")
        choosenNumber=int(input())
        if choosenNumber==1:
            startGame(connect4,GameMode.AI)
        elif choosenNumber==2:
            print("Enter the network IP:")
            ip=input()
            startGame(connect4,GameMode.NETWORK)
    elif choosenNumber==2:
        print("Select a game to load")
    else:
        print("Wrong choice.")