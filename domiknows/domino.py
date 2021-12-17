from domiknows.move import Move
from enum import Enum

class Domino:

	def __init__(self, t, b):
		"""Creates a new Domino. Dominoes are immutable, and can only be played/connected
		once. The layout of a domino, and it's connections are as follows:
			  T
			┌───┐
			│ t │
		  L ├───┤ R
			│ b │
			└───┘
			  B

		T,L,R,B are references to other dominoes, whereas t and b are numbers such
		that t < b"""

		self._t = t
		self._b = b

		self._T = self._L = self._R = self._B = None

		self.spinner = False
	
	@property
	def value(self):
		return (self._t, self._b)
	
	@property
	def connections(self):
		return [self._T, self._L, self._B, self._R]
	
	def connect(self, source):
		"""smart connects the source domino to the current domino, such that
		the orientation is not required. Returns the connection position as a 
		DominoOrientation, so that a move can be created"""
		pass
	
	def __repr__(self):
		return self.value.__str__() 

class DominoOrientation(Enum):
	
	TOP = "top"
	BOTTOM = "bottom"
	RIGHT = "right"
	LEFT = "left"
