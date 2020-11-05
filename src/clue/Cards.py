# Create Rooms
ROOMS = {
	'Hall',
	'Dining Room',
	'Billiards Room',
	'Ballroom',
	'Kitchen',
	'Study',
	'Conservatory',
	'Lounge',
	'Library'
}

# Create People
PEOPLE = {
	'Green',
	'Mustard',
	'Scarlet',
	'Plum',
	'White',
	'Peacock'
}

# Create Weapons
WEAPONS = {
	'Revolver',
	'Rope',
	'Lead Pipe',
	'Wrench',
	'Candlestick',
	'Knife'
}

# Create Deck with the Rooms, People, and Weapons
DECK = ROOMS.union(PEOPLE.union(WEAPONS))

# When we get an improper deck, raise an error
class InvalidTriple(ValueError):
	pass

class Triple:
	def __init__(self, person, weapon, room):
		if person not in PEOPLE:
			raise InvalidTriple("%s is not a person." % person)
		if weapon not in WEAPONS:
			raise InvalidTriple("%s is not a weapon." % weapon)
		if room not in ROOMS:
			raise InvalidTriple("%s is not a room." % room)
		self.person = person
		self.weapon = weapon
		self.room = room

	# Create a property with all the cards
	@property
	def all_cards(self):
		return [self.person, self.weapon, self.room]
	
	def __repr__(self):
		return "Triple(%r, %r, %r)" % (self.person, self.weapon, self.room)