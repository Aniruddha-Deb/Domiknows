from domiknows.board import Board
from domiknows.player import Player, HumanPlayer, ComputerPlayer
from domiknows.rule import Rule, TwoPlayerBlock, rules
from domiknows.domino import Domino
from domiknows.strategy import Strategy, GreedyStrategy

from os import environ
import json
from dotenv import load_dotenv, find_dotenv
from domiknows.rule import rules
from domiknows.strategy import strategies
from domiknows.player import HumanPlayer, ComputerPlayer

# some personal notes while developing:
#
# 1. DON't worry about the UI at this stage. It's nothing more than a facade, and
#    your objective is to develop an algorithm, not a fancy ui
# 2. Worry about ruleset and gameplay, not about control of flow or small things.

class Game:
	
	def __init__(self, config, ui):
		"""Initialize a new game, according to the configuration specified"""
		self.ui = ui
		self.config = config
		self.rule = rules[config.rule]()
		self.players = self._create_players(config.player_types_strategies)
		self.curr_player_move = None

		self.player_scores = [0]*len(self.players)
		self.player_hands_won = [0]*len(self.players)
		self.hands_sequence = []

		ui.game = self

	def play(self):
		ingame = True
		while (ingame):
			# make new pips, reset player pip set, etc
			self._init_new_board()
			inboard = True
			move_seq = self.rule.arbiter_moves(self)
			while (inboard):
				for pidx in move_seq:
					player = self.players[pidx]
					self.curr_player_move = player
					player_board_info = self.board.get_board_information(player)
					move = player.move(player_board_info)

					if self.rule.verify_move(self.board, move):
						self.board.move(move, player)
						self.player_scores[pidx] += self.rule.score_move(player_board_info, move)
					
					if self.rule.end_game(self):
						ingame = False
						inboard = False
						# TODO handle draws, or prove that a draw is impossible in 
						# this game (I think the latter is true, because of the turn
						# based nature)
						self.hands_sequence.append(player)
						self.winner = player
						break
					elif self.rule.end_board(self.board):
						inboard = False
						self.hands_sequence.append(player)
						end_board_scores = self.rules.score_end_of_board(self.board)
						for (score, curr_score) in zip(end_board_scores, self.player_scores):
							curr_score += score

						# check again if someone's won
						if self.rule.end_game(self):
							ingame = False
							self.winner = player
							break

		self.ui.display_winner(self.winner)

		print("Woohoo, nice game, gg")

	def _create_pips(self, pip_set):
		pips = []
		npips = int(pip_set[:len(pip_set)//2])
		for i in range(0, npips+1):
			for j in range(i, npips+1):
				pips.append(Domino(i,j))

		return pips
	
	def _create_players(self, pts):
		pid = 0
		game_players = []
		for desc in pts:
			type_strat = desc.split(':')
			if type_strat[0] == "HumanPlayer":
				game_players.append(HumanPlayer(pid, self.ui))
			elif type_strat[0] == "ComputerPlayer":
				game_players.append(ComputerPlayer(pid, strategies[type_strat[1]](self.rule)))
			pid += 1

		return game_players
	
	def _init_new_board(self):
		self.pips = self._create_pips(self.config.pip_set)
		print(self.pips)
		self.board = Board(self.pips, self.players)
		self.rule.deal_pips(self.board)
	
class GameConfiguration:

	# - Rule (All3, All5, Draw, Block)
	# - Pip set (66, 99, 1212 etc)
	# - PointLimit (100, 150, etc)
	# - HandLimit  (2,3,4,...)
	# - PlayerTypesStrategies: List ('ComputerPlayer:Strategy' for a computer player)
	#
	# TODO maybe in v2, have a chess timer type thing for move arbitration

	def __init__(self,
		rule = "TwoPlayerBlock",
		pip_set = "66",
		point_limit = 100,
		hand_limit = -1,
		player_types_strategies = ['HumanPlayer', 'HumanPlayer']):

		self.rule = rule 
		self.pip_set = pip_set 
		self.point_limit = point_limit 
		self.hand_limit = hand_limit 
		self.player_types_strategies = player_types_strategies 
	
	#def __init__(self, envname="test.env"):
	#	load_dotenv(envname)
	#	
	#	self.rule = environ.get('rule')
	#	self.pip_set = environ.get('pip_set')
	#	self.point_limit = int(environ.get('point_limit'))
	#	self.hand_limit = int(environ.get('hand_limit'))
	#	self.players_types_strategies = json.parse(environ.get('players_types_strategies'))

