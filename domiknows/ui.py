from domiknows.game import GameConfiguration

class UI:
	
	def __init__(self):
		print("Dominoes v.0.1")
		print("by Aniruddha Deb")
		print("-----------------------------------------")
		pass

class TextUI(UI):

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
	
	def render_game(self, game):
		print("Game, woooo!!!")
	
	def get_new_options_modal(self):
		return (input('Do you want to continue with the same options? ([y]/n): ') or 'y') == 'y'
	
	def prompt_new_game(self):
		return (input('Play again? ([y]/n): ') or 'y') == 'y'

	def render_pip(self, pip, orientation):
		"""Returns the domino as a string, with the given orientation. Possible
		orientations are in the enum DominoOrientation. The orientation
		specifies that the smaller number would be aligned to that position."""
		pass
