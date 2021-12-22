from abc import ABC, abstractmethod

players = {}
def player(cls):
    players[cls.__name__] = cls
    return cls

class Player(ABC):
	
	def __init__(self, pid):
		
		# assign pips later
		self.id = pid
		self.score = 0
		self.wins = 0
		self.pips = []

	@abstractmethod
	def move(self, board):
		"""performs a move on the board. This method is abstract, and needs to
		be implemented differently depending on the player"""
		pass
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		if isinstance(other, Player):
			return other.id == self.id
		return False

	def __ne__(self, other):
		return not self.__eq__(other)

@player
class HumanPlayer(Player):

	def __init__(self, pid, ui):
		super().__init__(pid)
		self.ui = ui

	def move(self, board):
		"""waits on user from ui interactively and plays move."""
		self.ui.render_game()
		input("Make a move ;)) : ")
		return None

@player
class ComputerPlayer(Player):
	
	def __init__(self, pid, strategy):
		super().__init__(pid)

		self.strategy = strategy
	
	def move(self, board):
		"""obtains the best move from the strategy that the computer player was 
		initialized with"""
		pass

# class Oracle(Player):
# 	"""The purpose of the oracle is to act as the third player, or the 'dealer'
# 	in this game. The first move made in the game is made by the oracle, when 
# 	it checks which side has the higher bone."""
# 	# DESIGN_QUESTION: should we have an oracle, or let the game handle this ?
# 	#
# 	# main reasons for not having the oracle: all the actions of the oracle are
# 	# interboard rather than intraboard, and these actions are generally handled 
# 	# by the game, rather than by a player (by definition, a player plays within
# 	# the scope of the board, and not across boards). 
# 	# 
# 	# yep, convinced myself that we don't need an oracle.		
