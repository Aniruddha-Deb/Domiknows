# The main entry point script

from domiknows.game import Game, GameConfiguration
from domiknows.ui import TwoPlayerTextUI

def test_main():
	ui = TwoPlayerTextUI()
	game_options = GameConfiguration() # default options

	new_game = True
	old_options = False
	while (new_game):

		if (old_options):
			continue_options = ui.get_new_options_modal()
			if (not continue_options):
				game_options = ui.get_game_options()
			else:
				old_options = False
			
		game = Game(game_options, ui)

		result = game.play()

		new_game = ui.prompt_new_game()
		old_options = True

def prod_main():
	ui = TextUI()
	game_options = ui.get_game_options()

	new_game = True
	old_options = False
	while (new_game):

		if (old_options):
			continue_options = ui.get_new_options_modal()
			if (not continue_options):
				game_options = ui.get_game_options()
			else:
				old_options = False
			
		game = Game(game_options, ui)

		result = game.play()

		new_game = ui.prompt_new_game()
		old_options = True

test_main()
