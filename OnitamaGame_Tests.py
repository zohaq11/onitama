"""
other_player
get_token
is_legal_move
move
get_winner
undo
"""
from OnitamaGame import OnitamaGame, Player

import random


def test_other_player() -> None:
    g = OnitamaGame()
    output = g.other_player(g.player1)
    assert output == g.player2
    g2 = OnitamaGame()
    output2 = g2.other_player(g2.player2)
    assert output2 == g2.player1
    g3 = OnitamaGame()
    output3 = g3.other_player(Player('invalid'))
    assert output3 is None


def test_get_token() -> None:
    g = OnitamaGame()
    assert g.get_token(0, 0) == 'x'
    assert g.get_token(0, 2) == 'X'
    assert g.get_token(4, 4) == 'y'
    assert g.get_token(4, 2) == 'Y'

    x = random.randint(1, 3)
    y = random.randint(1, 3)
    assert g.get_token(x, y) == ' '

    x = random.randint(-100, -1)
    y = random.randint(5, 100)
    assert g.get_token(x, y) == ' '

    x = random.randint(0, 4)
    y = random.randint(0, 4)
    assert isinstance(g.get_token(x, y), str)


def test_is_legal_move() -> None:
    g = OnitamaGame()
    x = random.randint(1, 3)
    y = random.randint(1, 3)
    assert g.is_legal_move(0, 0, x, y)

    x2 = random.randint(5, 100)
    y2 = random.randint(5, 100)
    assert not g.is_legal_move(x, y, x2, y2)


def test_move() -> None:
    g = OnitamaGame()
    assert g.move(0, 0, 1, 0, 'crab')
    assert g.move(4, 0, 3, 1, 'mantis')
    g2 = OnitamaGame()
    assert g2.move(0, 4, 1, 3, 'rooster')
    assert not g2.move(3, 4, 2, 3, 'mantis')


def test_get_winner() -> None:
    g = OnitamaGame()
    assert g.get_winner is None


def test_undo() -> None:
    g = OnitamaGame()
    g.undo()

    assert g.get_token(1, 0) == ' '
    assert g.move(0, 0, 1, 0, 'crab')
    assert g.get_token(1, 0) == 'x'
    g.undo()
    assert g.get_token(1, 0) == ' '


if __name__ == '__main__':
    import pytest
    pytest.main(['OnitamaGame_Tests.py'])
