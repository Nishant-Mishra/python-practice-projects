"""
    Inspired from https://twitter.com/RHDZMOTA/status/1429013476635119616 and https://xkcd.com/2496/
"""
import reprlib
from typing import Sequence, Union

MAX_NEIGHBOURS = 8
MINE = 'X'
SAFE = ' '


class Position:
    def __init__(self, pos: tuple[int, int] = (0, 0)):
        self._pos = list(pos)
        self._idx = 0

    def __getitem__(self, index: int):
        assert 0 <= index <= 2, "IndexError: Index for 'Position' objects can only be 0 or 1 representing x or y"
        return self._pos[index]

    def __add__(self, pos):
        return self.__class__(
            (self._pos[0] + pos[0], self._pos[1] + pos[1])
        )

    def __iadd__(self, pos):
        self._pos[0] += pos[0]
        self._pos[1] += pos[1]

    def __sub__(self, pos):
        return self.__class__(
            (self._pos[0] - pos[0], self._pos[1] - pos[1])
        )

    def __ge__(self, pos):
        return self._pos[0] >= pos[0] and self._pos[1] >= pos[1]

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx >= len(self._pos):
            raise StopIteration
        item = self._pos[self._idx]
        self._idx += 1

        return item

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self._pos)}"


class Grid:
    def __init__(self, grid: list[list[int]]):
        self._grid = grid

    def size(self):
        return len(self._grid), len(self._grid[0])

    def __getitem__(self, index: Union[Sequence, Position]):
        return self._grid[index[0]][index[1]]

    def __repr__(self):
        return f"{self.__class__.__name__}({reprlib.repr(self._grid)})"

    def __str__(self):
        to_print = []
        for row in self._grid:
            for elem in row:
                to_print.append(f" [{elem}]")
            to_print.append('\n')

        return ''.join(to_print)


# A num > 0, denotes number of mines surrounding it...
# A '0' denotes, unknown square...
# An 'X' denotes a Mine...
# A ' ' denotes No Mine...
grid = Grid([
    [2, 0, 1, 0],
    [0, 0, 3, 0],
    [3, 0, 0, 0],
    [0, 1, 0, 1]
])


class mine_map:
    def __init__(self, mapp: Grid):
        self._map = mapp

    def neighbours(self, pos: Position) -> list[Position]:
        neighb = []
        # Start from Top left diagonal neighbour
        next_pos = pos - (1, 1)
        inc_seq = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i in range(MAX_NEIGHBOURS):
            # Need this check as -ve indices are possible in Python Lists.
            if next_pos >= (0, 0):
                try:
                    _ = self._map[next_pos]
                except IndexError:
                    pass
                else:
                    neighb.append(next_pos)

            next_pos = next_pos + inc_seq[i // 2]

        return neighb

    def is_mine_possible(self, pos: tuple[int, int]) -> bool:
        if self._map[pos] != 0:
            return False

        pos = Position(pos)
        neighbours = self.neighbours(pos)
        no_mines = 0
        for n in neighbours:
            mines = self._map[n]
            if isinstance(mines, int) and mines > 0:
                neighb = self.neighbours(n)
                surrounding_mines = len([x for x in neighb if self._map[x] == MINE])
                if surrounding_mines >= mines:
                    return False
            elif mines == SAFE:
                no_mines += 1
                if no_mines == MAX_NEIGHBOURS:
                    return False

        return True

    def size(self):
        return self._map.size()


if __name__ == '__main__':
    m = mine_map(grid)
    print(f"{m.is_mine_possible((1, 1))}")
    print(grid)

    