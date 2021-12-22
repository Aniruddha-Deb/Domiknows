from domiknows.game import GameConfiguration
from domiknows.domino import Domino, DominoOrientation

class UI:
	
	def __init__(self):
		print("Dominoes v.0.1")
		print("by Aniruddha Deb")
		print("-----------------------------------------")

class TextUI(UI):

	def __init__(self):
		super().__init__()
		self.buffer = [[' ']*105 for i in range(39)]
		self.width = 105
		self.height = 39
		self.prev_game_info = None

		self._init_buffer()
		
	# curses-style indexing: (y,x)
	def print_text(self, text, pos):
		for i in range(pos[1], min(pos[1]+len(text),self.width)):
			self.buffer[pos[0]][i] = text[i-pos[1]]
	
	def blit(self, block, pos):
		for i in range(pos[0], min(pos[0]+len(block), self.height)):
			for j in range(pos[1], min(pos[1]+len(block[0]), self.width)):
				self.buffer[i][j] = block[i-pos[0]][j-pos[1]]
	
	def clear(self, tl, br):
		for i in range(min(tl[0], self.height), min(br[0], self.height)):
			for j in range(min(tl[1], self.width), min(br[1], self.width)):
				self.buffer[i][j] = ' '
	
	def _init_buffer(self):
		for i in range(self.height):
			self.buffer[i][12] = self.buffer[i][79] = '║'

		for i in range(13):
			self.buffer[16][i] = self.buffer[22][i] = '═'

		self.buffer[16][12] = self.buffer[22][12] = '╣'

		self.print_text("Boneyard", (0,86))

	def get_game_options(self):
		opt = {}
		
		opt['rule'] = input('rule [Block]: ') or 'Block'
		opt['pip_set'] = input('pip_set [66]: ') or '66'
		opt['point_limit'] = int(input('point_limit [100]: ') or 100)
		opt['hand_limit'] = int(input('hand_limit [-1]: ') or -1)

		num_players = int(input('num_players [2]: ') or 2)
		pts = []
		for i in range(num_players):
			ptype = input(f'player{i+1}_type [HumanPlayer]: ') or 'HumanPlayer'
			if (ptype == 'ComputerPlayer'):
				pstrat = input('player_strategy [GreedyStrategy]:') or 'GreedyStrategy'
				pts.append(f"{ptype}:{pstrat}")
			else:
				pts.append(ptype)
		opt['player_types_strategies'] = pts

		return GameConfiguration(**opt)
	
	# TODO implement renderer according to the format laid out in shell script
	def render_game(self):
		self._update_buffer_with_game_contents(self.game)
		self._print_buffer()
	
	def _update_buffer_with_game_contents(self, game):

		
		self.print_text("Player 1", (28,2))
		self.print_text("Player 2", (9,2))
		self.print_text(str(game.player_scores[0]),(29,5))
		self.print_text(str(game.player_scores[1]),(10,5))

		board_info = game.board.get_board_information(game.curr_player_move)

		# print boneyard
		byx = 81
		byy = 9
		nb = 0
		print(board_info.boneyard_count)
		for b in range(board_info.boneyard_count):
			bone_block = self.render_pip(None, DominoOrientation.LEFT, hidden=True)
			self.blit(bone_block, (byy+(nb//2)*3, byx+(nb%2)*10))
			nb += 1
	
		cp_by = 34
		player_bones = None
		for bone in board_info.self_pips:
			bone_block = self.render_pip(bone, DominoOrientation.TOP, hidden=False)
			if not player_bones:
				player_bones = bone_block
			else:
				for a,b in zip(player_bones, bone_block):
					a.extend(b)

		for i in range(len(player_bones)):
			l = player_bones[i]
			player_bones[i] = list(("".join(l)).center(66))

		self.blit(player_bones, (cp_by, 13))

		opp_bones = None
		# TODO extend this layout to more than two players: currently, the UI 
		# cannot handle more than four players. Too much flexibility, rip
		opp_pip_count = [board_info.player_pip_count[k] 
						 for k in board_info.player_pip_count.keys()
						 if k != game.curr_player_move][0]

		for b in range(opp_pip_count):
			bone_block = self.render_pip(None, DominoOrientation.TOP, hidden=True)
			if not opp_bones:
				opp_bones = bone_block
			else:
				for a,b in zip(opp_bones, bone_block):
					a.extend(b)

		for i in range(len(opp_bones)):
			l = opp_bones[i]
			opp_bones[i] = list(("".join(l)).center(66))

		self.blit(opp_bones, (2, 13))

		self.prev_game_info = board_info
					
		
	def _print_buffer(self):
		for a in self.buffer:
			print(''.join(a))
	
	def get_new_options_modal(self):
		return (input('Do you want to continue with the same options? ([y]/n): ') or 'y') == 'y'
	
	def prompt_new_game(self):
		return (input('Play again? ([y]/n): ') or 'y') == 'y'

	def render_pip(self, pip, orientation, hidden=False):
		"""Returns the domino as a string, with the given orientation. Possible
		orientations are in the enum DominoOrientation. The orientation
		specifies that the smaller number would be aligned to that position."""
		
		block = None
		if (orientation == DominoOrientation.LEFT or orientation == DominoOrientation.RIGHT):
			if (hidden):
				block = [ list("┌───────┐"),
						  list("│       │"),
						  list("└───────┘")  ]
			elif orientation == DominoOrientation.LEFT:
				block = [ list("┌───┬───┐"),
						  list(f"│{str(pip.value[0]).center(3)}│{str(pip.value[1]).center(3)}│"),
						  list("└───┴───┘")  ]
			elif orientation == DominoOrientation.RIGHT:
				block = [ list("┌───┬───┐"),
						  list(f"│{str(pip.value[1]).center(3)}│{str(pip.value[0]).center(3)}│"),
						  list("└───┴───┘")  ]

		elif (orientation == DominoOrientation.TOP or orientation == DominoOrientation.BOTTOM):
			if (hidden):
				block = [ list("┌───┐"),
						  list("│   │"),
						  list("│   │"),
						  list("│   │"),
						  list("└───┘")  ]
			elif orientation == DominoOrientation.TOP:
				block = [ list("┌───┐"),
						  list(f"│{str(pip.value[0]).center(3)}│"),
						  list("├───┤"),
						  list(f"│{str(pip.value[1]).center(3)}│"),
						  list("└───┘")  ]
			elif orientation == DominoOrientation.BOTTOM:
				block = [ list("┌───┐"),
						  list(f"│{str(pip.value[1]).center(3)}│"),
						  list("├───┤"),
						  list(f"│{str(pip.value[0]).center(3)}│"),
						  list("└───┘")  ]

		return block

