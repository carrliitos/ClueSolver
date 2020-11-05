import pytest

from src.clue import Cards

class TestTriple:
	'''The first three tests are to make sure we catch invalid triples'''
	def test_invalid_person(self):
		with pytest.raises(Cards.InvalidTriple):
			Cards.Triple('Invalid', 'Rope', 'Hall')

	def test_invalid_weapon(self):
		with pytest.raises(Cards.InvalidTriple):
			Cards.Triple('Green', 'Invalid', 'Hall')

	def test_invalid_room(self):
		with pytest.raises(Cards.InvalidTriple):
			Cards.Triple('Green', 'Rope', 'Invalid')

	'''The remaining are to make sure that each action of the method under test
	behaves as expected.'''
	def test_person(self):
		t = Cards.Triple('Green', 'Rope', 'Hall')
		assert t.person == 'Green'

	def test_weapon(self):
		t = Cards.Triple('Green', 'Rope', 'Hall')
		assert t.weapon == 'Rope'

	def test_room(self):
		t = Cards.Triple('Green', 'Rope', 'Hall')
		assert t.room == 'Hall'

	def test_all_cards(self):
		t = Cards.Triple('Green', 'Rope', 'Hall')
		assert t.all_cards == ['Green', 'Rope', 'Hall']

	def test_repr(self):
		t = Cards.Triple('Green', 'Rope', 'Hall')
		assert repr(t) == "Triple('Green', 'Rope', 'Hall')"