import clue.Cards as Cards
from clue.Exceptions import ImpossibleError

# Player class
class Player:
	def __init__(self, name, numCards):
		self.name = name
		# number of cards this player holds
		self.numCards = numCards
		# Set of cards this player is known to have
		self.hasCards = set()
		# Set of cards this player is known NOT to have
		self.notHasCards = set()
		# list of triple as about
		self.asked = []
		# list of triples of which one has been shown to someone
		self.shown = []

	def hasCard(self, card):
		self.hasCards.add(card)
		if len(self.hasCards) > self.numCards:
			raise ImpossibleError(
				"%s has only %s cards but has shwon %r" % 
				(self.name, self.numCards, self.hasCards))

	def ask(self, triple):
		self.asked.append(triple)

	def show(self, triple):
		if set(triple.all_cards).issubset(self.notHasCards):
			raise ImpossibleError(
				"%s showed me one of %s, but earlier decline to show all those."
				% (self.name, triple))

		self.shown.append(triple)

	def noshow(self, triple):
		has = self.hasCards.intersection(triple.all_cards)
		if has:
			raise ImpossibleError(
				"%s declined for %s, but we know they have %s"
				% (self.name, triple.all_cards, has))

		self.notHasCards.update(triple.all_cards)

	def check(self):
		impossible = self.hasCards.intersection(self.notHasCards)
		if impossible:
			raise ImpossibleError(
				"%s is known to have and known to not have %s"
				% (self.name, impossible))

	def snapshot(self):
		s = self.__class__(self.name, self.numCards)
		s.hasCards = self.hasCards.copy()
		s.notHasCards = self.notHasCards.copy()
		s.asked = self.asked.copy()
		s.shown = self.shown.copy()
		return s

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.name, self.numCards)

class Me(Player):
	def __init__(self, myCards):
		myCards = set(myCards)
		super().__init__("Me", len(myCards))
		self.hasCards.update(myCards)
		self.notHasCards = set(Cards.DECK).difference(self.hasCards)

	def snapshot(self):
		s = self.__class__(self.hasCards)
		s.asked = self.asked.copy()
		s.shown = self.shown.copy()
		return s

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, sorted(self.hasCards))