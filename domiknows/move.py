class Move:

	# want a move to be immutable, hence all the private variables and their 
	# getters
	def __init__(self, played, source, target, position, score, mno=0):
		
		self._played = played
		self._source = source
		self._target = target
		self._position = position
		self._move_no = mno
		self._score = score
	
	@property
	def played(self):
		return self._played

	@property
	def source(self):
		return self._source

	@property
	def target(self):
		return self._target

	@property
	def position(self):
		return self._position

	@property
	def move_no(self):
		return self._move_no

	@property
	def score(self):
		return self._score

	@property
	def move_tuple(self):
		return (self._move_no, self._played, self._source, self._target, self._position, self._score)
