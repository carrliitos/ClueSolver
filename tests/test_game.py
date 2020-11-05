import pytest

from clue.Exceptions import ImpossibleError
from clue.Player import Player, Me
from clue import Cards
from clue import Game

class TestGame:
	'''Test class to make sure the game behaves properly'''
	def test_others(self):
		'''Testing other players'''
		g = Game.Game(Me({}), [Player("Foo", 4), Player("Bar", 14)])

		assert len(g.others) == 2
		assert g.others[0].name == "Foo"
		assert g.others[0].numCards == 4
		assert g.others[1].name == "Bar"
		assert g.others[1].numCards == 14

	def test_me(self):
		'''Testing my behaviors as a player'''
		g = Game.Game(Me({'Plum'}), [Player("Foo", 17)])

		assert g.me.numCards == 1
		assert g.me.hasCards == {'Plum'}

	def test_wrong_number_card(self):
		'''Test behavior when we have the wrong number of cards'''
		with pytest.raises(ImpossibleError):
			Game.Game(Me({}), [Player("Foo", 3)])

	def test_dupe_player_names(self):
		'''Test behavior when multiple other names are identical'''
		with pytest.raises(ImpossibleError):
			Game.Game(Me({}), [Player("Foo", 3), Player("Foo", 13)])

	def test_snapshot(self):
		'''Test a game state snapshot'''
		g = Game.Game(Me({'White'}), [Player("Foo", 17)])
		g2 = g.snapshot()
		t = Cards.Triple('White', 'Rope', 'Hall')

		g.me.ask(t)
		g.others[0].show(t)

		assert not g2.me.asked
		assert not g2.others[0].shown

	def test_repr(self):
		g = Game.Game(Me({'White'}), [Player("Foo", 17)])

		assert repr(g) == "Game(Me(['White']), [Player('Foo', 17)])"