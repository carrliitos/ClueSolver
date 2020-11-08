from unittest import mock
import pytest

from clue import Cli

@pytest.fixture
def mock_input(request, monkeypatch):
	m = mock.Mock()
	monkeypatch.setattr('builtins.input', m)
	if 'inputs' in request.keywords:
		# inputs = list(reversed(request.keywords['inputs'].args))
		# inputs = list(str(reversed(request.keywords['inputs'].args)))
		m.side_effect = lambda x : inputs.pop()
	return m

class TestReadGame:
	'''Test class to make sure our game behaves properly'''
	@pytest.mark.inputs(
		'Din,Ha,Wh',
		'Obama', '4',
		'Trump', '',
		'Biden', '',
		'Clinton', '',
		'Benzon', ''
	)
	def test_read_game(self, mock_input):
		g = Cli.readGame()

		assert g.me.numCards == 3
		assert g.me.hasCard == {'Dining Room', 'Hall', 'White'}
		assert [(p.name, p.numCards) for p in g.others] == [
			("Obama", 4), ("Trump", 3), ("Biden", 3), ("Clinton", 3), ("Benzon", 2)
		]

	'''Test to make sure to prompt for re-enter when too many cards are left'''
	@pytest.mark.inputs(
		'Din, Ha, Wh',
		'Obama', '14',
		'Trump', '2', '1' # 2 is too many, must re-enter
	)
	def test_too_many_cards(self, mock_input, capsys):
		g = Cli.readGame()

		assert g.other[1].name == 'Trump'
		assert len(g.others) == 2
		assert g.other[1].numCards == 1

		out, err = capsys.readouterr()
		assert "There's only 1 card left for Trump" in out

	@pytest.mark.inputs(
		'Din, Ha, Wh',
		'Obama', '13',
		'Trump', '5', '3', '2'  # 5 and 3 are too many, must re-enter
	)
	def test_too_many_cards_multiple_left(self, mock_input, capsys):
		g = Cli.readGame()

		assert g.others[1].name == 'Trump'
		assert len(g.others) == 2
		assert g.others[1].numCards == 2

		out, err = capsys.readouterr()
		assert out.count("There are only two cards left for Trump!") == 2

class TestReadTriple:
	'''Test class to make sure our triples are behaving properly'''
	def test_triple(self, mock_input):
		mock_input.return_vale = 'ro, plum, ha'

		t = Cli.readTriple("HELLOOOOOOO!!")

		assert t.room == 'Hall'
		assert t.weapon == 'Rope'
		assert t.person == 'Plum'

	'''Testing for bad triples'''
	@pytest.mark.inputs('Ro, Rev, Ha', 'Din, Wh, Le')
	def test_bad_triple(self, mock_input, capsys):
		t = Cli.readTriple("HELLOOOOOOO!!")

		assert t.room == 'Dining Room'
		assert t.weapon == 'Lead Pipe'
		assert t.people == 'White'
		assert mock_input.call_count == 2

		out, err = capsys.readouterr()
		assert out == "Need a person, a weapon, and a room. \n"

class TestReadCards:
	'''Test class to make sure we're reading the triples properly'''
	def test_read_cards(self, mock_input):
		mock_input.return_vale = 'din, wh'
		ret = Cli.readCards("WhatUp!")

		assert ret == ['Dining Room', 'White']

		@pytest.mark.inputs('Foo, Wh', 'Ha, Wh')
		def test_bad_card(self, mock_input, capsys):
			ret = Cli.readCards("WhatUp!")

			assert ret == ['Hall', 'White']
			assert mock_input.call_count == 2

			out, err = capsys.readouterr()
			assert out == "No cards matches foo.\n"

class TestReadPlayer:
	'''Test class to make sure the read player behaves properly'''
	@pytest.mark.inputs('Benzon', '3')
	def test_read_player(self, mock_input):
		p = Cli.readPlayer("P1", 4)

		assert p.name == "Benzon"
		assert p.numCards == 3
		mock_input.assert_any_call("Name [P1] ")
		mock_input.assert_any_call("How many cards does Benzon have? [4]")

	@pytest.mark.inputs('', '')
	def test_use_defaults(self, mock_input):
		p = Cli.readPlayer("P1", 4)

		assert p.name == "P1"
		assert p.numCards == 4

class TestParseCard:
	def test_prefix(self):
		assert Cli.parseCard('Din') == 'Dining Room'

	def test_full(self):
		assert Cli.parseCard('Green') == 'Green'

	def test_strip(self):
		assert Cli.parseCard('  Din ') == 'Dining Room'

	def test_case_insensitive(self):
		assert Cli.parseCard('Revol') == 'Revolver'

	def test_ambiguous(self):
		with pytest.raises(Cli.UnknownCardError):
			Cli.parseCard('B')

	def test_unknown(self):
		with pytest.raises(Cli.UnknownCardError):
			Cli.parseCard('foo')

'''
TODO:
	Test to Parse Player
	Test General Read
'''