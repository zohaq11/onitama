from Player import Player
from typing import List, Union
from Style import Style
from Pieces import Pieces


class SizeError(Exception):
    """Exception that is raised when size is too small or is odd."""
    pass


class OnitamaBoard:
    """
    An OnitamaBoard class consisting of a game board, and keeping track of player token information and styles.
    It can set and clear the board and check if potential plays are valid through coordinate checking.

    === Attributes ===
    size : A board's width and height.
    player1 : Player object representing player who will play the G1 and M1 pieces.
    player2 : Player object representing player who will play the G2 and M2 pieces.
    styles :  A list of all possible play styles including: dragon, crab, horse, mantis, rooster.

    === Private Attributes ===
    _board :
        A nested list representing a grid layout for the board.

    === Representation Invariants ===
    - Size is always an odd number greater or equal to 5.
    - player1 has G1 and M1 pieces.
    - player2 has G2 and M2 pieces.
    """
    size: int
    player1: Player
    player2: Player
    styles: List[Style]
    _board: List[List[str]]

    def __init__(self, size: int, player1: Player, player2: Player, board: Union[List[List[str]], None] = None) -> None:
        """
        Constructs an empty Onitama board. Places four monks and one grandmaster
        on opposite sides of the board. Creates five Styles and distributes them
        among the players.
        """

        if size % 2 == 0 or size < 5:
            raise SizeError
        else:
            self.size = size
        self.player1 = player1
        self.player2 = player2

        if board:
            self.set_board(board)
        else:
            self._board = []
            for r in range(size):
                row = []
                for c in range(size):
                    # place grandmasters
                    if r == 0 and c == size//2:
                        row.append(Pieces.G1)
                    elif r == size - 1 and c == size//2:
                        row.append(Pieces.G2)

                    # place monks
                    elif r == 0:
                        row.append(Pieces.M1)
                    elif r == size - 1:
                        row.append(Pieces.M2)
                    else:
                        row.append(Pieces.EMPTY)

                self._board.append(row)

        self.styles = []
        self.construct_styles()

    def construct_styles(self) -> None:
        """
        Constructs the 5 movement styles of Onitama for this board. Normally,
        there are 16 movement styles and they are distributed randomly, however for
        this assignment, you are only required to use 5 of them (Dragon, Crab, Horse,
        Mantis, and Rooster).

        You can find the movement patterns for these styles under assets/{style}.png,
        where {style} is one of the five styles mentioned above. Additionally, you
        can also find the images in README.md.

        IMPORTANT: Additionally, we are going to distribute the styles at the start
        of the game in a static or consistent manner. Player 1 (G1) must get the Crab
        and Horse styles. Player 2 (G2) must get the Mantis and Rooster styles. Extra
        (EMPTY) must get the Dragon style.

        Please be sure to follow the distribution of styles as mentioned above as
        this is important for testing. Failure to follow this distribution of styles
        will result in the LOSS OF A LOT OF MARKS.
        >>> g = OnitamaBoard(5, Player('player1'), Player('player2'))
        >>> len(g.styles) == 5
        True
        >>> for s in g.styles:
        ...     if s.name == 'crab' or s.name == 'horse':
        ...         s.owner == Pieces.G1
        ...     elif s.name == 'mantis' or s.name == 'rooster':
        ...         s.owner == Pieces.G2
        ...     else:
        ...         s.owner == ' '
        True
        True
        True
        True
        True
        """

        self.styles.append(Style([(1, 1), (1, -1), (-1, 2), (-1, -2)], 'dragon'))
        self.styles.append(Style([(-1, 0), (0, -2), (0, 2)], 'crab', Pieces.G1))
        self.styles.append(Style([(-1, 0), (1, 0), (0, -1)], 'horse', Pieces.G1))
        self.styles.append(Style([(1, 0), (-1, 1), (-1, -1)], 'mantis', Pieces.G2))
        self.styles.append(Style([(0, 1), (0, -1), (-1, 1), (1, -1)], 'rooster', Pieces.G2))

    def exchange_style(self, style: Style) -> bool:
        """
        Exchange the given <style> with the empty style (the style whose owner is
        EMPTY). Hint: Exchanging will involve swapping the owners of the styles.

        Precondition: <style> cannot be the empty style.
        >>> g = OnitamaBoard(5, Player('player1'), Player('player2'))
        >>> for s in g.styles:
        ...     if s.owner == ' ':
        ...         prev_empty = s
        >>> prev_owner = g.styles[1].owner
        >>> g.styles[1].owner != ' '
        True
        >>> g.exchange_style(g.styles[1])
        True
        >>> g.styles[1].owner == ' '
        True
        >>> prev_empty.owner == prev_owner
        True

        >>> g.exchange_style(g.styles[-1])
        True
        >>> g.styles[-1].owner == ' '
        True
        """
        for s in self.styles:
            if s.owner == Pieces.EMPTY:
                s.owner = style.owner
                style.owner = Pieces.EMPTY
                return True
        return False

    def valid_coordinate(self, row: int, col: int) -> bool:
        """
        Returns true iff the provided coordinates are valid (exists on the board).
        >>> b = OnitamaBoard(5, Player('player1'), Player('player2'))
        >>> b.valid_coordinate(0, 0)
        True
        >>> b.valid_coordinate(4, 4)
        True
        >>> b.valid_coordinate(5, 5)
        False
        """

        return 0 <= row < self.size and 0 <= col < self.size

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the player token that is in the given <row> <col> position, or the empty
        character if no player token is there or if the position provided is invalid.
        >>> g = OnitamaBoard(5, Player('player1'), Player('player2'))
        >>> g.get_token(0, 0)
        'x'
        >>> g.get_token(4, 4)
        'y'
        >>> g.get_token(1, 1)
        ' '
        >>> g.get_token(-1, -5)
        ' '
        """

        if 0 <= row < self.size and 0 <= col < self.size:
            return self._board[row][col]
        else:
            return Pieces.EMPTY

    def set_token(self, row: int, col: int, token: str) -> None:
        """
        Sets the given position on the board to be the given player (or throne/empty)
        <token>.
        >>> g = OnitamaBoard(5, Player('player1'), Player('player2'))
        >>> g.get_token(0, 0)
        'x'
        >>> g.set_token(0, 0, ' ')
        >>> g.get_token(0, 0)
        ' '
        >>> g.set_token(1, 1, 'x')
        >>> g.get_token(1, 1)
        'x'
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            self._board[row][col] = token

    def get_styles_deep_copy(self) -> List[Style]:
        """
        DO NOT MODIFY THIS!!!
        Returns a deep copy of the styles of this board.
        """
        return [style.__copy__() for style in self.styles]

    def deep_copy(self) -> List[List[str]]:
        """
        DO NOT MODIFY THIS!!!
        Creates and returns a deep copy of this OnitamaBoard's
        current state.
        """
        return [row.copy() for row in self._board]

    def set_board(self, board: List[List[str]]) -> None:
        """
        DO NOT MODIFY THIS!!!
        Sets the current board's state to the state of the board which is passed in as a parameter.
        """
        self._board = [row.copy() for row in board]

    def __str__(self) -> str:
        """
        Returns a string representation of this game board.
        """
        s = '  '
        for col in range(self.size):
            s += str(col) + ' '

        s += '\n'

        s += ' +'
        for col in range(self.size):
            s += "-+"

        s += '\n'

        for row in range(self.size):
            s += str(row) + '|'
            for col in range(self.size):
                s += self._board[row][col] + '|'

            s += str(row) + '\n'

            s += ' +'
            for col in range(self.size):
                s += '-+'

            s += '\n'

        s += '  '
        for col in range(self.size):
            s += str(col) + ' '

        s += '\n'
        return s
