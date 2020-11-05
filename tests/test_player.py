import pytest

from clue.Cards import Triple, DECK
from clue.Exceptions import ImpossibleError
from clue import Player

'''Test class for the player'''
class TestPlayer:
	'''Test for player having cards'''
	def test_has_card(self):
		p = Player.Player("Foo", 3)

		p.hasCard('Green')

		assert p.hasCards == {'Green'}

	'''Test for exception error when player has too many cards'''
	def test_has_too_many(self):
		p = Player.Player("Foo", 3)
		
		p.hasCard('Green')
		p.hasCard('Hall')
		p.hasCard('White')

		with pytest.raises(ImpossibleError):
			p.hasCard('Rope')

	'''Test when player has identical cards'''
	def test_has_identical(self):
		p = Player.Player("Foo", 3)

		p.hasCard('Green')
		p.hasCard('Green')

		assert p.hasCards == {'Green'}

	'''Test when a player asks another player'''
	def test_ask(self):
		p = Player.Player("Foo", 3)
		t = Triple('White', 'Rope', 'Hall')

		p.ask(t)

		assert p.asked == [t]

	'''Test when a player shows another player their cards'''
	def test_show(self):
		p = Player.Player("Foo", 3)
		t = Triple('White', 'Rope', 'Hall')

		p.show(t)

		assert p.shown == [t]

	'''Test for an impossible error for notHasCards'''
	def test_show_impossible(self):
		p = Player.Player("Foo", 3)
		t = Triple('White', 'Rope', 'Hall')

		p.notHasCards = {'Green', 'White', 'Rope', 'Hall'}

		with pytest.raises(ImpossibleError):
			p.show(t)

	'''Test when player decides not to show their cards'''
	def test_noshow(self):
		p = Player.Player("Foo", 3)
		t = Triple('White', 'Rope', 'Hall')

		p. noshow(t)

		assert p.notHasCards == {'White', 'Rope', 'Hall'}

	'''Test for ImpossibleError when player decides not to show their cards'''
	def test_noshow_impossible(self):
		p = Player.Player("Foo", 3)
		t = Triple('White', 'Rope', 'Hall')

		p.hasCards = {'Rope'}

		with pytest.raises(ImpossibleError):
			p.noshow(t)

	'''Test when a player checks their cards'''
	def test_check_good(self):
		p = Player.Player("Foo", 3)

		p.hasCards = {'Green', 'Rope'}
		p.notHasCards == {'White', 'Revolver'}

		p.check()

	'''Test if hasCards and notHasCards have similar cards when player checks'''
	def test_check_bad(self):
		p = Player.Player("Foo", 3)

		p.hasCards = {'White', 'Rope'}
		p.notHasCards = {'White', 'Revolver'}

		with pytest.raises(ImpossibleError):
			p.check()

	'''Test string representation'''
	def test_repr(self):
		p = Player.Player("Foo", 3)

		assert repr(p) == "Player('Foo', 3)"

'''Test class for me as a player'''
class TestMe:
	'''Test to make sure me is initialized'''
	def test_init(self):
		m = Player.Me({'White', 'Green', 'Hall'})

		assert m.hasCards == {'White', 'Green', 'Hall'}
		assert m.numCards == 3
		assert m.notHasCards == set(DECK).difference(m.hasCards)

	'''Test when we've been duped!'''
	def test_dupes(self):
		m = Player.Me({'White', 'Green', 'Hall', 'White'}) # Two 'White'

		assert m.hasCards == {'White', 'Green', 'Hall'}
		assert m.numCards == 3
		assert m.notHasCards == set(DECK).difference(m.hasCards)

	'''Test string representation'''
	def test_repr(self):
		m = Player.Me(['Plum', 'Wrench', 'Hall'])

		assert repr(m) == "Me(['Hall', 'Plum', 'Wrench'])"