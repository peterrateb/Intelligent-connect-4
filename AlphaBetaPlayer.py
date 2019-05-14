
import random
import itertools
import timeit
import copy
from connect4 import Connect4

class SearchTimeout(Exception):
	#An exception rasied when time out
	pass

evaluationTable = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3]
]

class Player:
	"""Player Class
	"""

	#def __init__(self, timeout=30000.,search_depth=3,):
	def __init__(self, level = 'MED',search_depth=3):
		self.search_depth = search_depth
		if (level == 'EASY'):
			self.TIMER_THRESHOLD = 3000
			self.evaluate=self.evaluate_easy
		elif (level== 'MED'):
			self.TIMER_THRESHOLD = 10000
			self.evaluate=self.evaluate_medium
		elif (level== 'HARD'):
			self.TIMER_THRESHOLD = 30000
			self.evaluate=self.evaluate_hard

	def time_millisec(self):
		return 1000 * timeit.default_timer()
	def time_used(self,time_start):
		return self.time_millisec() - time_start
	def evaluate_easy(self,gameState):
                # Evaluation value
                evaluteValue = 0
                # First player
                if gameState.turn==1 :
                    # Iterate through the board to find red and blue disc
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 1 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 2 :
                                # add losing state
                                evaluteValue -= evaluationTable[i][j]
                # Second Player
                else:
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 2 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 1 :
                                # add losing state
                                evaluteValue -= evaluationTable[i][j]
                '''
                The function returns player's winning value
                evaluteValue = 0 : Wining state is equal for both playes
                evaluteValue > 0 : Player has a high wining propability
                evaluteValue < 0 : Player has a low  wining propability
                '''
                return evaluteValue
	def evaluate_medium(self,gameState):
                # Evaluation value
                evaluteValue = 0
                # First player
                if gameState.turn==1 :
                    # Iterate through the board to find red and blue disc
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 1 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 2 :
                                # add losing state
                                evaluteValue -= (evaluationTable[i][j])**2
                # Second Player
                else:
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 2 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 1:
                                # add losing state
                                evaluteValue -= (evaluationTable[i][j])**2
                '''
                The function returns player's winning value
                evaluteValue = 0 : Wining state is equal for both playes
                evaluteValue > 0 : Player has a high wining propability
                evaluteValue < 0 : Player has a low  wining propability
                '''
                return evaluteValue
	def evaluate_hard(self,gameState):
                # Evaluation value
                evaluteValue = 0
                # First player
                if gameState.turn==1 :
                    # Iterate through the board to find red and blue disc
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 1 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 2 :
                                # add losing state
                                evaluteValue -= (evaluationTable[i][j])**3
                # Second Player
                else:
                    for i in range(6):
                        for j in range(7):
                            if gameState.board[i][j]== 2 :
                                # add wining state
                                evaluteValue += evaluationTable[i][j]
                            elif gameState.board[i][j] == 1 :
                                # add losing state
                                evaluteValue -= (evaluationTable[i][j])**3
                '''
                The function returns player's winning value
                evaluteValue = 0 : Wining state is equal for both playes
                evaluteValue > 0 : Player has a high wining propability
                evaluteValue < 0 : Player has a low  wining propability
                '''
                return evaluteValue


class AlphaBetaPlayer(Player):
	"""Game-playing agent that chooses a column to play
	using iterative deepening minimax search with alpha-beta pruning.
	"""
	NOCOLUMNS=7
	def get_col(self, gameState):
		"""Get the best column to play
		"""
		time_start = self.time_millisec()
		best_play = -1
		depth=1
		try:
			while (True):
				col = self.alphabeta(gameState, time_start, depth)
				if col is not -1:
					best_play = col
				if self.time_used(time_start) > self.TIMER_THRESHOLD:
					raise SearchTimeout()
                #iterative deepening
				depth+=1
		except SearchTimeout:
			return best_play
		# Return the best move from the last completed search iteration
		return best_play

	def alphabeta(self, gameState,time_start, depth, alpha=float("-inf"), beta=float("inf")):
		"""depth-limited minimax search with alpha-beta pruning
		"""
		if self.time_used(time_start) > self.TIMER_THRESHOLD:
			raise SearchTimeout()

		best_score = float("-inf")
		best_play = None
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			if (gameState.detect_valid_first_row(col)) != -1 :
				#if valid column
				newGameState = copy.deepcopy(gameState)
				newGameState.play(col)
			v = self.min_value(newGameState,time_start, depth - 1 , alpha , beta)
			alpha = max ( alpha , v)
			if v > best_score:
				best_score = v
				best_play = col
			if beta <= alpha:
				break
		if best_play==None:
			return -1
		return best_play
	
	
	def min_value(self,gameState,time_start,depth,alpha,beta):
		"""
		return the minimum value over all legal childnodes.
		"""
		v= float('Inf')
		if depth==0 or not gameState.is_any_place_empty() :
			return self.evaluate(gameState)
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			newGameState = copy.deepcopy(gameState)
			newGameState.play(col)
			v = min(v,self.max_value(newGameState,time_start,depth-1,alpha,beta))
			if v<= alpha :
				return v
			beta = min (beta, v)
		return v
	
	
	def max_value(self,gameState,time_start,depth,alpha,beta):
		"""
		Return the maximum value over all legal child nodes.
		"""
		v= float('-Inf')
		if depth==0 or not gameState.is_any_place_empty() :
			return self.evaluate(gameState)
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			newGameState = copy.deepcopy(gameState)
			newGameState.play(col)
			v = max(v,self.min_value(newGameState,time_start,depth-1,alpha,beta))
			if v>= beta:
				return v
			alpha = max ( alpha , v)
		return v
