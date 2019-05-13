
import random
import itertools
import timeit
from connect4 import Connect4



class SearchTimeout(Exception):
	#An exception rasied when time out
	pass



class Player:
	"""Player Class
	Parameters
	----------
	search_depth : int (optional), initialized = 3

	timeout : float (optional)
		Time remaining (in milliseconds) when search is aborted, initialized = 3000.
	"""
    #def __init__(self, search_depth=3, score_fn= evaluate, timeout=30.):
	def __init__(self, search_depth=3, timeout=3000.):
		self.search_depth = search_depth
		#self.score = score_fn
		#self.time_left = None
		self.TIMER_THRESHOLD = timeout
	def time_millisec(self):
		return 1000 * timeit.default_timer()
	def time_used(self,time_start):
		return self.time_millisec() - time_start


class AlphaBetaPlayer(Player):
	"""Game-playing agent that chooses a column to play
	using iterative deepening minimax search with alpha-beta pruning.
	"""
	NOCOLUMNS=7
	def get_col(self, gameState):
		"""Get the best column to play
		Parameters
		----------
		gameState : A state of `connect 4 Board` encoding the current state of the game.

		Returns
		-------
		(int, int)
			Board coordinates corresponding to a legal move; may return
			(-1, -1) if there are no available legal moves.
		"""
		time_start = self.time_millisec()
		best_play = -1
		depth=1
		try:
			# The try/except block will automatically catch the exception
			# raised when the timer is about to expire.
			#for depth in itertools.repeat(1):
			while (True):
				col = self.alphabeta(gameState, time_start, depth)
				if col is not -1:
					best_play = col
				if self.time_used(time_start) > self.TIMER_THRESHOLD:
					raise SearchTimeout()
					#return best_move
                #iterative deepening
				depth+=1
		except SearchTimeout:
			return best_play
			# Handle any actions required after timeout as needed

		# Return the best move from the last completed search iteration
		return best_play

	def alphabeta(self, gameState,time_start, depth, alpha=float("-inf"), beta=float("inf")):
		"""depth-limited minimax search with alpha-beta pruning

		Parameters
		----------
		gameState : Connect4
			An instance of the Connect4 game `Board` class representing the
			current game state

		time_start : start time of the turn to play in milliseconds

		depth : int
			depth of search

		alpha : float
			Alpha limits the lower bound of search on minimizing layers, initialized = -inf

		beta : float
			Beta limits the upper bound of search on maximizing layers, initialized = -inf

		Returns
		-------
		int
			The column number of the best play found in the current search;
			-1 if there are no play chances

		"""
		if self.time_used(time_start) > self.TIMER_THRESHOLD:
			raise SearchTimeout()

		best_score = float("-inf")
		best_play = None
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			#m = self.get_move(game,self.time_left)
			if (gameState.detect_valid_first_row(col)) != -1 :
				#if valid column
				v = self.min_value(gameState.play(col),time_start, depth - 1 , alpha , beta)
			#if v>= beta:
			#	break
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
		#if self.terminal_test(game):
		#	return self.score(game,self)
		if depth==0 or not gameState.is_any_place_empty() :
			return gameState.evaluate()
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			#move = self.get_move(game,self.time_left)
			newgameState = gameState.play(col)
			v = min(v,self.max_value(newgameState,time_start,depth-1,alpha,beta))
			if v<= alpha :
				return v
			beta = min (beta, v)
		return v
	
	
	def max_value(self,gameState,time_start,depth,alpha,beta):
		"""
		Return the maximum value over all legal child nodes.
		"""
	
		v= float('-Inf')
		#if self.terminal_test(game):
		#	return self.score(game,self)
		if depth==0 or not gameState.is_any_place_empty() :
			return gameState.evaluate()
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			#move = self.get_move(game,self.time_left)
			newgameState = gameState.play(col)
			v = max(v,self.min_value(newgameState,time_start,depth-1,alpha,beta))
			if v>= beta:
				return v
			alpha = max ( alpha , v)
		return v
	
