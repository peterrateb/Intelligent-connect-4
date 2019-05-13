
import random
import itertools
import timeit
from connect4 import Connect4



class SearchTimeout(Exception):
	#An exception rasied when time out
	pass



class Player:
	"""Player Class
	"""

	def __init__(self, search_depth=3, timeout=3000.):
		self.search_depth = search_depth
		self.TIMER_THRESHOLD = timeout
	def time_millisec(self):
		return 1000 * timeit.default_timer()
	def time_used(self,time_start):
		return self.time_millisec() - time_start
	def evaluate(self,gameState):
		pass


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
				v = self.min_value(gameState.play(col),time_start, depth - 1 , alpha , beta)
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
		if depth==0 or not gameState.is_any_place_empty() :
			return self.evaluate(gameState)
		for col in range(self.NOCOLUMNS):
			if self.time_used(time_start) > self.TIMER_THRESHOLD:
				raise SearchTimeout()
			newgameState = gameState.play(col)
			v = max(v,self.min_value(newgameState,time_start,depth-1,alpha,beta))
			if v>= beta:
				return v
			alpha = max ( alpha , v)
		return v
	
