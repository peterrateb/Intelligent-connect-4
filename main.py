from connect4 import Connect4
from AlphaBetaPlayer import AlphaBetaPlayer
from enum import Enum
from communication import networkAgent
from gevent.server import DatagramServer
import colorama
from colorama import Fore, Back
import gevent
import json
import sys

received_data = ""


class Server(DatagramServer):
    def handle(self, data, address):
        global received_data
        received_data = json.loads(data.decode())


class GameMode(Enum):
    AI = 0
    NETWORK = 1


def AIMode(connect4, playerTurn, difficulty):
    if playerTurn == True:
        connect4.turn = 1
    else:
        connect4.turn = 2
    connect4.print_board()
    while connect4.is_any_place_empty():
        col_no = -1
        AI = AlphaBetaPlayer(difficulty)
        if (playerTurn):
            col_no = input("Your turn, please enter a column number, or 's' to save game and exit.")
            if col_no == 's':
                connect4.save()
                return
            else:
                col_no = int(col_no) - 1
        else:
            print("AI turn, please wait.")
            col_no = AI.get_col(connect4)

        while not (connect4.play(col_no)):
            col_no = input(
                "Your turn, Invalid disk location please enter a valid column number, or 's' to save game and exit.")
            if col_no == 's':
                connect4.save()
                return
            else:
                col_no = int(col_no) - 1
        connect4.print_board()
        if connect4.check_winner() == True:
            if (playerTurn):
                print("You Wins.")
            else:
                print("AI Wins.")
            sys.exit(0)
        playerTurn = not playerTurn
        connect4.change_turn()
    if connect4.check_winner() == True:
        if (playerTurn):
            print("You Wins.")
        else:
            print("AI Wins.")
    else:
        print("No one win")


def NetworkMode(connect4, ip, localPort, networkPort, ourTurn, difficulty):
    agent = networkAgent(ip, networkPort)
    server = Server(':' + str(localPort))  # creates a new server
    server.start()
    # if ourTurn == True:
    #     connect4.turn = 1
    # else:
    #     connect4.turn = 2
    connect4.print_board()
    while connect4.is_any_place_empty():
        col_no = -1
        AI = AlphaBetaPlayer(difficulty)
        if ourTurn:
            print("Our Turn.")
            col_no = AI.get_col(connect4)
            connect4.play(col_no)
            agent.send(connect4.board, col_no + 1)
        else:
            print("Opponent turn, please wait.")
            while 1:
                gevent.sleep(0)
                global received_data
                if received_data == "":
                    continue
                for dict in received_data:
                    if dict['type'] == 'MV':
                        col_no = dict['content']
                        connect4.play(col_no - 1)
                received_data = ""
                break

        connect4.print_board()
        if connect4.check_winner() == True:
            if (ourTurn):
                print("You Wins.")
            else:
                print("You Lose.")
            sys.exit(0)
        ourTurn = not ourTurn
        connect4.change_turn()
    if connect4.check_winner() == True:
        if (ourTurn):
            print("You Wins.")
        else:
            print("You Lose.")
    else:
        print("No one win")


def startGame(connect4, mode, startFirst, difficulty):
    if mode == GameMode.AI:
        AIMode(connect4, startFirst, difficulty)
    else:
        localPort = int(input("Please enter the local port:"))
        networkPort = int(input("Please enter the port of destination machine:"))
        ip = input("Please enter the ip address of destination machine:")

        NetworkMode(connect4, ip, localPort, networkPort, startFirst, difficulty)


if __name__ == "__main__":
    colorama.init(autoreset=True)  # Automatically adds a Style.RESET_ALL after each print statement
    print("Welcome to Connect 4 game")
    print("Please choose option number.")
    print("1.New Game")
    print("2.Load Game")
    choosenNumber = input()
    choosenNumber = int(choosenNumber)
    connect4 = Connect4()
    if choosenNumber == 1:
        # New Game option
        print("Please choose option number.")
        print("1.BEGINNER")
        print("2.EASY")
        print("3.MEDIUM")
        print("4.HARD")
        choosenNumber = int(input())
        difficulty = 'MED'
        if choosenNumber == 1:
            difficulty = 'BEGINNER'
        elif choosenNumber == 2:
            difficulty = 'EASY'
        elif choosenNumber == 3:
            difficulty = 'MED'
        else:
            difficulty = 'HARD'
        print("Please choose option number.")
        print("1.VS Local AI")
        print("2.VS Network AI")
        choosenNumber = int(input())
        if choosenNumber == 1:
            # VS Local AI
            print("Please choose option number.")
            print("1.Start first")
            print("2.Start second")
            startFirst = int(input())
            if startFirst == 1:
                startFirst = True
                startGame(connect4, GameMode.AI, startFirst, difficulty)
            elif startFirst == 2:
                startFirst = False
                startGame(connect4, GameMode.AI, startFirst, difficulty)
            else:
                print("Wrong Choice")
        elif choosenNumber == 2:
            # VS Network AI
            print("Please choose option number.")
            print("1.Start first")
            print("2.Start second")
            startFirst = int(input())
            if startFirst == 1:
                startFirst = True
                startGame(connect4, GameMode.NETWORK, startFirst, difficulty)
            elif startFirst == 2:
                startFirst = False
                startGame(connect4, GameMode.NETWORK, startFirst, difficulty)
            else:
                print("Wrong Choice")
    elif choosenNumber == 2:
        print("Please choose option number.")
        difficulty = 'MED'
        print("1.BEGINNER")
        print("2.EASY")
        print("3.MEDIUM")
        print("4.HARD")
        choosenNumber = int(input())
        difficulty = 'MED'
        if choosenNumber == 1:
            difficulty = 'BEGINNER'
        elif choosenNumber == 2:
            difficulty = 'EASY'
        elif choosenNumber == 3:
            difficulty = 'MED'
        else:
            difficulty = 'HARD'
        # Load a saved game
        try:
            fh = open('connect4.txt', 'r')
            # Store configuration file values
            connect4.load()
            startGame(connect4, GameMode.AI, connect4.turn == 1, difficulty)
        except FileNotFoundError:
            print("No game saved found.")
    else:
        print("Wrong choice.")
