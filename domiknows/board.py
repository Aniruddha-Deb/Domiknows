class Board:

	def __init__(self, pips, players):
		"""Create a new board with the given rules. Note that a board refers to 
		a single 'hand' of dominoes, and state is not saved across boards (unless
		the game chooses to do so)"""
		self.players = players

		# set more attributes
		self.all_pips = pips

		self.pip_graph = None
		self.boneyard = []

		self.sum = 0
		self.curr_move = 0

		self.ends = []
		self.move_history = []

	def draw(self, player):
		"""Draw a single pip from the boneyard."""
		pass
	
	def move(self, board, player):
		"""chains the source domino (from the player) to the target domino (already
		on the board). Position is not required, due to the uniqueness of the 
		target and the source."""
		pass
	
	def get_moves(self, pips):
		"""Returns a list of all possible moves, for a player who has the following
		set of pips"""
		pass

	def get_board_information(self, player):
		
		info = BoardInformation(self)
		info.self_pips = player.pips
		info.player_pip_count = {p : len(p.pips) for p in self.players}
		return info
	
class BoardInformation:
	
	def __init__(self, board):

		self.pip_graph = board.pip_graph
		self.boneyard_count = len(board.boneyard)
		self.player_count = len(board.players)
		self.move_history = board.move_history
		# should board/boardinfo have rules as well? strategy would need the 
		# rules to work (different rules would have different strategies, fml)
		# Let game handle all that... board would not have rules.
		self.sum = board.sum
		self.ends = board.ends
