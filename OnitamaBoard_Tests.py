"""
construct_styles
exchange_Style
valid_coordinate
get_token
set_token
"""
from OnitamaBoard import OnitamaBoard, Player, Pieces

import random


def test_construct_styles() -> None:
    b = OnitamaBoard(5, Player('player1'), Player('player2'))
    assert len(b.styles) == 5
    for s in b.styles:
        if s.name == 'crab' or s.name == 'horse':
            assert s.owner == Pieces.G1
            assert (-1, 0) in s.get_moves()
        elif s.name == 'mantis' or s.name == 'rooster':
            assert s.owner == Pieces.G2
        else:
            assert s.owner == ' '
            assert s.get_moves() == [(1, 1), (1, -1), (-1, 2), (-1, -2)]

    b.construct_styles()
    assert len(b.styles) == 10


def test_exchange_style() -> None:
    b = OnitamaBoard(5, Player('player1'), Player('player2'))
    x = random.randint(0, 4)

    while b.styles[x].owner == ' ':
        x = random.randint(0, 4)
    prev_empty = ''
    for s in b.styles:
        if s.owner == ' ':
            prev_empty = s
    prev_owner = b.styles[x].owner
    assert b.styles[x].owner != ' '
    assert b.exchange_style(b.styles[x])

    assert b.styles[x].owner == ' '

    assert prev_empty.owner == prev_owner


def test_valid_coordinate() -> None:
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    b = OnitamaBoard(5, Player('player1'), Player('player2'))
    assert b.valid_coordinate(x, y)

    x = random.randint(-100, -1)
    y = random.randint(-100, -1)
    assert not b.valid_coordinate(x, y)

    x = random.randint(5, 100)
    y = random.randint(5, 100)
    assert not b.valid_coordinate(x, y)

    assert b.valid_coordinate(0, 0)
    assert b.valid_coordinate(4, 4)


def test_get_token() -> None:
    b = OnitamaBoard(5, Player('player1'), Player('player2'))

    assert b.get_token(0, 0) == 'x'
    assert b.get_token(0, 2) == 'X'
    assert b.get_token(4, 4) == 'y'
    assert b.get_token(4, 2) == 'Y'

    x = random.randint(1, 3)
    y = random.randint(1, 3)
    assert b.get_token(x, y) == ' '

    x = random.randint(-100, -1)
    y = random.randint(5, 100)
    assert b.get_token(x, y) == ' '

    x = random.randint(0, 4)
    y = random.randint(0, 4)
    assert isinstance(b.get_token(x, y), str)


def test_set_token() -> None:
    g = OnitamaBoard(5, Player('player1'), Player('player2'))
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    g.set_token(x, y, ' ')
    assert g.get_token(x, y) == ' '

    x = random.randint(0, 4)
    y = random.randint(0, 4)
    g.set_token(x, y, 'x')
    assert g.get_token(x, y) == 'x'

    x = random.randint(0, 4)
    y = random.randint(0, 4)
    g.set_token(x, y, 'y')
    assert g.get_token(x, y) == 'y'


if __name__ == '__main__':
    import pytest
    pytest.main(['OnitamaBoard_Tests.py'])
