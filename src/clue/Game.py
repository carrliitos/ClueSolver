import clue.Cards as Cards
from clue.Exceptions import ImpossibleError

# Game class
class Game:
	'''
	Provide a list of players and cards.
	Each player should be a (name, # of cards) tuple
	'''
	numPlayerCards = len(Cards.DECK) - 3

	def __init__(self, me, others):
		self.others = others
		self.othersByName = {p.name for p in others}
		
		if len(self.othersByName) != len(self.others):
			raise ImpossibleError("Player names must be unique!")

		self.me = me
		totalCards = self.me.numCards + sum([p.numCards for p in self.others])
		if totalCards != self.numPlayerCards:
			raise ImpossibleError(
				"%s cards held by players should be %s."
				%(totalCards, self.numPlayerCards)
				)

	def snapshot(self):
		return self.__class__(self.me.snapshot(), 
			[p.snapshot() for p in self.others])

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.me, self.others)