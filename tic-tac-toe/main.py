#!/usr/bin/env python
import random
from itertools import repeat
from math import sqrt
from typing import Union
from constants import *


class TicTacToe:

    def __init__(self, blocks = 9):
        assert (rows := sqrt(blocks)) == int(rows), \
            "ValueError: The number of blocks in TicTacToe must be a perfect square"
        self._size = blocks
        self._rows = self._cols = int(rows)
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
        top_line = ''.join(list(repeat(' ' * block_width + '|', self._cols - 1))) + ' ' * block_width
        bottom_line = ''.join(list(repeat('_' * block_width + '|', self._cols - 1))) + '_' * block_width
        for i in range(self._rows):
            print(top_line)
            for j in range(self._cols):
                print(f"{self._board[i * self._cols + j]:^{block_width}}", end='')
                print("|" if j != self._cols - 1 else '', end='')
            print()
            print(top_line if i == self._rows - 1 else bottom_line)

        return ''

    def _validate_row_col(self, row: Union[int, slice], col: Union[int, slice]):
        if isinstance(row, int):
            assert row < self._rows, f"ValueError: Invalid row number '{row}' for board size '{self._size}'"

        if isinstance(col, int):
            assert col < self._cols, f"ValueError: Invalid col number '{col}' for board size '{self._size}'"

    def _get_row(self, row: int):
        self._validate_row_col(row, 0)
        return [self._board[i] for i in range(row * self._cols, (row + 1) * self._cols)]

    def _get_col(self, col: int):
        self._validate_row_col(0, col)
        return [self._board[j] for j in range(col, self._rows * self._cols, self._rows)]

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
            return self._board[row * self._cols + col]

    def __setitem__(self, key: int, val):
        assert key <= self._size, f"Invalid cell number '{key}', valid range: (1 - {self._size})"
        if isinstance(key, slice):
            raise NotImplementedError("__setitem__() not supported with 'slice'. "
                                      "Specify 'key' as 'int'")

        self._board[key] = val

    @property
    def left_diagonal(self):
        return [self._board[i] for i in range(0, self._size, self._cols + 1)]

    @property
    def right_diagonal(self):
        return [self._board[i] for i in range(self._cols - 1, self._size, self._cols - 1)][:-1]

    @property
    def size(self):
        return self._size

    def __str__(self):
        return self.show_board()


class GamePlay:

    def __init__(self):
        self._symbol = {Player.COMPUTER: '', Player.USER: ''}
        self._ttt = TicTacToe()
        self._current_player = random.choice([
            Player.COMPUTER, Player.USER
        ])

    def welcome(self):
        print(f"Welcome to Tic Tac Toe")
        self._symbol[Player.USER] = input(f"Choose your playing character (usually 'X' or 'O'): ")
        self._symbol[Player.COMPUTER] = 'X' if self._symbol[Player.USER] != 'X' else 'O'
        print()
        print(f"{Player.USER.value} will use '{self._symbol[Player.USER]}', "
              f"{Player.COMPUTER.value} will use '{self._symbol[Player.COMPUTER]}'")
        print()

    def _get_user_pos(self):
        user_pos = None
        while True:
            user_pos = int(input(f"Enter the position of your input (1-{self._ttt.size}): "))
            if user_pos > self._ttt.size or user_pos < 1:
                print("Invalid input, try again !!")
            else:
                break
        return user_pos

    def _computer_choice(self):
        available_choices = [pos + 1 for pos, elem in enumerate(self._ttt[:, :]) if not elem]
        return random.choice(available_choices)

    def run_game(self):
        self.welcome()
        input("Press Enter to begin the match...")
        print(f"{self._current_player.value} will start the match !!")
        print(self._ttt)
        while True:
            if self._current_player == Player.USER:
                next_pos = self._get_user_pos()
            else:
                next_pos = self._computer_choice()
            print(f"{self._current_player.value} chose position '{next_pos}'")
            self._ttt[next_pos - 1] = self._symbol[self._current_player]
            print(self._ttt)
            self._current_player = Player.USER if self._current_player == Player.COMPUTER else Player.COMPUTER



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
    repr(game)


def main():
    test_rig()
    g = GamePlay()
    g.run_game()


if __name__ == '__main__':
    main()