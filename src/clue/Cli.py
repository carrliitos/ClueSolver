from clue.Cards import DECK, ROOMS, WEAPONS, PEOPLE, Triple
from clue.Game import Game
from clue.Player import Player, Me

class CliError(Exception):
	pass

class UnknownCardError(CliError):
	pass

class UnknownPlayerError(CliError):
	pass

def readGame():
	'''	Query the user about the initial game setup (players and cards).'''
	myCards = readCards("My cards (comma-separated): ")
	print("My cardsa re %r" % myCards)
	me = Me(myCards)
	others = []
	cardsSoFar = me.numCards
	print("Tell me about the other players, starting from my left.")
	
	while cardsSoFar < Game.numPlayerCards:
		defaultName = "Player %s" % (len(others) + 1)
		maxCards = Game.numPlayerCards - cardsSoFar
		defaultNumCards = min(3, maxCards)
		player = readPlayer(defaultName, defaultNumCards, maxCards=maxCards)
		others.append(player)
		cardsSoFar += player.numCards

	return Game(me, others)

def readTriple(prompt):
	'''Query user for a person/weapon/room triple.'''
	while True:
		cards = readCards(prompt)
		rooms = [c for c in cards if c in ROOMS]
		weapons = [c for c in cards if c in WEAPONS]
		people = [c for c in cards if c in PEOPLE]

		if any(len(l) != 1 for l in [rooms, weapons, people]):
			print("Need a person, a weapon, and a room.")
			continue

		return Triple(people[0], weapons[0], rooms[0])

def readCards(prompt):
	'''Query user for any non-empty list of valid cards.'''
	while True:
		numCards = _read(
			"How many cards does %s have?" % name,
			default = defaultNumCards,
			coerceTo = int
			)
		print("got %s" % numCards)
		if maxCards and numCards > maxCards:
			if maxCards == 1:
				msg = "There's only 1 card"
			else:
				msg = "There are only %s cards" % maxCards

			print("%s left for %s!" % (msg, name))
			continue

		return Player(name, numCards)

def parseCard(prefix):
	'''Parse a valid card from given unambiguous prefix.'''
	return _parse(prefix, DECK, UnknownCardError, 'card')

def parsePlayer(prefix):
	'''Parse a valid player from given unambiguous prefix.'''
	return _parse(prefix, names, UnknownPlayerError, 'player')

def _read(prompt, default=None, required=False, coerceTo=str):
	'''Read a value from the input with a default, and optional type coercion'''
	if default is not None:
		fullPrompt = "%s [%s] " % (prompt, default)
	else:
		fullPrompt = "%s " % prompt

	while True:
		raw = input(fullPrompt)
		try:
			val = coerceTo(raw) if raw else default
		except(TypeError, ValueError):
			print("Sorry, I don't understand that.")
		else:
			if required and not val:
				print("Cant go on without an answer!")
			else:
				return val

def _parse(prefix, options, exceptionClass, optionType):
	'''Select one of ''options'' based on unambiuous ''prefix''.'''
	canonical = prefix.lower().strip()
	candidates = [o for o in options if o.lower().startswith(canonical)]
	if len(candidates) > 1:
		raise exceptionClass("More than one %s matches %s.") % (optionType, prefix)
	elif not candidates:
		raise exceptionClass("No %s matches %s." % (optionType, prefix))
	return candidates[0]