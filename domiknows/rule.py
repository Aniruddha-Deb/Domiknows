from abc import ABC, abstractmethod
from random import shuffle
from math import ceil

rules = {}
def rule(cls):
    rules[cls.__name__] = cls
    return cls

class Rule(ABC):

	def __init__(self):
		pass
	
	@abstractmethod
	def verify_move(self, board_info, move):
		"""Verifies the move according to the given ruleset."""
		pass
	
	@abstractmethod
	def score_move(self, board_info, move):
		"""scores the move. The score is an integer"""
		pass
	
	def get_moves(self, board_info):
		"""Gets a list of valid moves according to the board information visible.
		Returns an empty list if no moves are possible"""
		# TODO implement with a simple pip matching method for now, as that's the
		# most common move search algo
		pass
	
	@abstractmethod
	def arbiter_moves(self, game):
		"""Returns a sequence of player indices (0-indexed). This represents the 
		move sequence for this board. The game is passed instead of the board,
		as the first move may depend on previous board wins as well"""
		pass

	@abstractmethod
	def end_board(self, board):
		"""Checks if in the current state, the board has ended and a particular 
		player has won the game. Perfect information is needed for this, which 
		is why board rather than board_info is passed. This is also abstract, as
		different rules would have different criteria for the board to be ended."""
		pass
	
	@abstractmethod
	def score_end_of_board(self, board):
		"""returns scores of players at the end of the board. Generally, the 
		player with the least sum of pips gets all the points. Returns an array
		with player points"""
		pass
	
	@abstractmethod
	def deal_pips(self, board):
		"""deals the pips out to players. This dealing may vary depending on
		game rules, which is why this method is here"""
		pass
	
	@abstractmethod
	def end_game(self, game):
		"""Checks if the game has ended. Criteria can be different for different
		games: most games have a point limit, but some may have a hand limit as
		well"""
		pass
	
# TODO implement the simple block game here.
@rule
class Block(Rule):

	def verify_move(self, board_info, move):
		print("verifying move")
		return True

	def score_move(self, board_info, move):
		print("scoring move")
		return 0
	
	def arbiter_moves(self, game):
		return range(len(game.players))
	
	def end_board(self, board):
		pass
	
	def score_end_of_board(self, board):
		pass
	
	def deal_pips(self, board):
		shuffle(board.all_pips)
		set_size = len(board.all_pips)
		num_players = len(board.players)

		# splitting rules (something that extends to other sets as well)
		# for now, let ideal be 1:1:...:2 atmost. 
		# 28,2 -> 7:7:14 (ceil(28/4) = 7)
		# 28,3 -> 6:6:6:10 (ceil(28/5) = 6)
		# 28,4 -> 5:5:5:5:8 (ceil(28/6) = 5)
		#
		# 36,5 -> 6:6:6:6:6:6
		# 36,4 -> same as above
		# 36,3 -> 8:8:8:12

		num_pips_per_person = ceil(set_size/(num_players+2))
		for i in range(num_players):
			board.players[i].pips = board.all_pips[i*num_pips_per_person : (i+1)*num_pips_per_person]
		board.boneyard = board.all_pips[num_players*num_pips_per_person : ]
	
	def end_game(self, game):
		pass

