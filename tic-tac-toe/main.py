#!/usr/bin/env python
import random
from itertools import repeat
from math import sqrt
from typing import Union, Generator
from constants import *


class TicTacToe:

    def __init__(self, blocks = 9):
        assert (rows := sqrt(blocks)) == int(rows), \
            "ValueError: The number of blocks in TicTacToe must be a perfect square"
        self._size = blocks
        self._nrows = self._ncols = int(rows)
        self._board = [''] * self._size

    def show_board(self):
        """
            Display the board as shown:

                0  |  X  |  0
              _____|_____|_____
                   |     |
                X  |  0  |  X
              _____|_____|_____
                   |     |
                0  |  X  |  X

        """
        block_width = 7
        top_line = ''.join(list(repeat(' ' * block_width + '|', self._ncols - 1))) + ' ' * block_width
        bottom_line = ''.join(list(repeat('_' * block_width + '|', self._ncols - 1))) + '_' * block_width
        for i in range(self._nrows):
            print(top_line)
            for j in range(self._ncols):
                print(f"{self._board[i * self._ncols + j]:^{block_width}}", end='')
                print("|" if j != self._ncols - 1 else '', end='')
            print()
            print(top_line if i == self._nrows - 1 else bottom_line)

        return ''

    def _validate_row_col(self, row: Union[int, slice], col: Union[int, slice]):
        if isinstance(row, int):
            assert row < self._nrows, f"ValueError: Invalid row number '{row}' for board size '{self._size}'"

        if isinstance(col, int):
            assert col < self._ncols, f"ValueError: Invalid col number '{col}' for board size '{self._size}'"

    def _get_row(self, row: int) -> list[str]:
        self._validate_row_col(row, 0)
        return [self._board[i] for i in range(row * self._ncols, (row + 1) * self._ncols)]

    def _get_col(self, col: int) -> list[str]:
        self._validate_row_col(0, col)
        return [self._board[j] for j in range(col, self._nrows * self._ncols, self._nrows)]

    def __getitem__(self, key: tuple[Union[int, slice], Union[int, slice]]):
        row, col = key
        self._validate_row_col(row, col)

        if isinstance(row, slice) and any((row.start, row.stop, row.step)) or \
           isinstance(col, slice) and any((col.start, col.stop, col.step)):
            raise NotImplementedError("Multi-row, multi-col or block selection not supported, "
                                      "Use ':' only to select either a complete row or a complete column")

        if isinstance(row, slice) and isinstance(col, slice):
            return self._board.copy()

        elif isinstance(row, slice):
            return self._get_col(col)

        elif isinstance(col, slice):
            return self._get_row(row)

        else:
            return self._board[row * self._ncols + col]

    def __setitem__(self, key: int, val):
        assert key <= self._size, f"Invalid cell number '{key}', valid range: (1 - {self._size})"
        if isinstance(key, slice):
            raise NotImplementedError("__setitem__() not supported with 'slice'. "
                                      "Specify 'key' as 'int'")

        self._board[key] = val

    def rows(self) -> Generator:
        for i in range(self._nrows):
            yield self._get_row(i)

    def cols(self) -> Generator:
        for i in range(self._ncols):
            yield self._get_col(i)

    def diagonals(self) -> Generator:
        yield self.left_diagonal
        yield self.right_diagonal

    def all_combos(self):
        yield from self.rows()
        yield from self.cols()
        yield from self.diagonals()

    @property
    def corners(self) -> dict[int, str]:
        corners = [1,
                   self._ncols,
                   self._size - self._ncols + 1,
                   self._size]
        d = {}
        for c in corners:
            d[c] = self._board[c - 1]
        return d

    @property
    def mids(self) -> dict[int, str]:
        mids = [(self._ncols + 1) // 2,
                (self._nrows // 2) * self._ncols + 1,
                ((self._nrows // 2) + 1) * self._ncols,
                self._size - (self._ncols // 2)]
        d = {}
        for m in mids:
            d[m] = self._board[m - 1]
        return d

    @property
    def center(self) -> dict[int, str]:
        key = (self._size + 1) // 2
        return { key : self._board[key - 1] }


    @property
    def left_diagonal(self) -> list[str]:
        return [self._board[i] for i in range(0, self._size, self._ncols + 1)]

    @property
    def right_diagonal(self) -> list[str]:
        return [self._board[i] for i in range(self._ncols - 1, self._size, self._ncols - 1)][:-1]

    @property
    def size(self):
        return self._size

    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return self._ncols

    def __str__(self):
        return self.show_board()


# TODO:
#  - Add smart position selection for Computer and introduce Hard level
#  - Add a medium level which choses the position by randomly selecting Easy or Hard Algo.

class GamePlay:

    def __init__(self):
        self._symbol = {Player.COMPUTER: '', Player.USER: ''}
        self._ttt = TicTacToe()
        self._current_player = random.choice([
            Player.COMPUTER, Player.USER
        ])
        self._game_logic = GameLogic(self._ttt)

    @property
    def available_choices(self):
        available = [pos + 1 for pos, elem in enumerate(self._ttt[:, :]) if not elem]
        return available

    def welcome(self):
        print(f"Welcome to Tic Tac Toe")
        self._symbol[Player.USER] = input(f"Choose your playing character (usually 'X' or 'O'): ")
        self._symbol[Player.COMPUTER] = 'X' if self._symbol[Player.USER] != 'X' else 'O'
        print()
        print(f"{Player.USER.value} will use '{self._symbol[Player.USER]}', "
              f"{Player.COMPUTER.value} will use '{self._symbol[Player.COMPUTER]}'")
        print()

    def _get_user_choice(self):
        user_pos = None
        while True:
            user_pos = int(input(f"Enter the position of your input (1-{self._ttt.size}): "))
            if user_pos > self._ttt.size or user_pos < 1:
                print("Invalid input, try again !!")
            elif user_pos not in self.available_choices:
                print(f"This position is taken, try another...")
            else:
                break
        return user_pos

    def _computer_choice(self):
        return random.choice(self.available_choices)

    def run_game(self):
        self.welcome()
        print(f"{self._current_player.value} will start the match !!")
        input("Press Enter to begin the match...")
        print(self._ttt)
        while True:
            if self._current_player == Player.USER:
                next_pos = self._get_user_choice()
            else:
                next_pos = self._computer_choice()
            print(f"{self._current_player.value} chose position '{next_pos}'")
            self._ttt[next_pos - 1] = self._symbol[self._current_player]
            print(self._ttt)
            self._current_player = Player.USER if self._current_player == Player.COMPUTER else Player.COMPUTER

            winner = self._get_winner()
            if winner == Player.USER:
                print(f" B-(   You really think you can beat me... Have guts to try again ???")
                break
            elif winner == Player.COMPUTER:
                print(f" 8-D   I am God, you puny human !!!")
                break
            else:
                if not self.available_choices:
                    print(" B-|   Looks like you hit a luck, you are safe from my wrath today !!!")
                    break

    def _get_winner(self):
        winner = None
        # Check rows
        for i in range(self._ttt.nrows):
            row = self._ttt[i, :]
            if row[0] and len(set(row)) == 1:
                winner = row[0]
                break

        if not winner:
            # Check cols
            for j in range(self._ttt.ncols):
                col = self._ttt[:, j]
                if col[0] and len(set(col)) == 1:
                    winner = col[0]
                    break

        if not winner:
            # Check left_diagonal
            ld = self._ttt.left_diagonal
            if ld[0] and len(set(ld)) == 1:
                winner = ld[0]

        if not winner:
            # Check right_diagonal
            rd = self._ttt.right_diagonal
            if rd[0] and len(set(rd)) == 1:
                winner = rd[0]

        if winner:
            return Player.USER if winner == self._symbol[Player.USER] else Player.COMPUTER
        else:
            return None


class GameLogic:
    def __init__(self, ttt: TicTacToe):
        self._ttt = ttt


class GameLogicEasyLevel(GameLogic):
    """
    Play Defensive, i.e.
        - If possible, go for Win
        - ElIf possible, avoid defeat
        - Else, choose randomly when there are multiple options

    """
    def strategy(self):
        pass


def test_rig():
    game = TicTacToe()
    print(game)
    print(f"{game[1, 2] = }")
    print(f"{game[2, 0] = }")
    game[2] = 'X'
    game[4] = 'O'
    game[5] = 'X'
    game[8] = 'O'
    game[0] = 'X'
    game[6] = 'X'
    print(game)
    print(f"{game[:, 1] = }")
    print(f"{game[2, :] = }")
    print(f"{game[:, :] = }")
    # print(f"{game[:, 1] = }")
    # print(f"{game[0, :] = }")
    # print(f"{game[:, :] = }")
    # game[1, :] = ['X', '0', 'X']
    # game[:, 0] = ['X', '0', 'X']
    # game[:, :] = ['X', '0', 'X']
    # game[1:, :] = ['X', '0', 'X']
    print(f"{game.left_diagonal = }")
    print(f"{game.right_diagonal = }")
    print(f"{game.rows() = }")
    print(f"{list(game.rows()) = }")
    print(f"{game.cols() = }")
    print(f"{list(game.cols()) = }")
    print(f"{game.diagonals() = }")
    print(f"{list(game.diagonals()) = }")
    print(f"{game.all_combos() = }")
    print(f"{list(game.all_combos()) = }")
    print(f"{game.corners = }")
    print(f"{game.mids = }")
    print(f"{game.center = }")

    repr(game)


def main():
    test_rig()
    # g = GamePlay()
    # g.run_game()


if __name__ == '__main__':
    main()