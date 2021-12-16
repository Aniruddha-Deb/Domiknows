from abc import ABC, abstractmethod

strategies = {}
def strategy(cls):
    strategies[cls.__name__] = cls
    return cls

class Strategy(ABC):

	def __init__(self, rule):
		self.rule = rule
		pass
	
	@abstractmethod
	def best_move(self, board_info):
		"""gets the best move based on the current board. The baord has the 
		history, so it's not exactly completely positional, like chess."""

@strategy
class GreedyStrategy(Strategy):

	def best_move(self, board_info):
		pass

@strategy
class MinimaxStrategy(Strategy):

	def best_move(self, board_info):
		pass

