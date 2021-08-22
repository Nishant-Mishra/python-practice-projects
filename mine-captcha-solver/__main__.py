"""
    Inspired from https://twitter.com/RHDZMOTA/status/1429013476635119616 and https://xkcd.com/2496/
"""

MAX_NEIGHBOURS = 8

grid = [
    [2, 0, 1, 0],
    [0, 0, 3, 0],
    [3, 0, 0, 0],
    [0, 1, 0, 1]
]


class mine_map:
    def __init__(self, mapp: list[list[int]]):
        self._map = mapp

    def neighbours(self, pos: tuple[int, int]) -> tuple:
        neighb = []
        # Start from Top left diagonal neighbour
        next_pos = (pos[0] - 1, pos[1] - 1)
        inc_seq = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i in range(MAX_NEIGHBOURS):
            # Need this check as -ve indices are possible in Python Lists.
            if next_pos[0] >= 0 and next_pos[1] >= 0:
                try:
                    val = self._map[next_pos[0]][next_pos[1]]
                except IndexError:
                    pass
                else:
                    neighb.append(next_pos)
            next_pos = (next_pos[0] + inc_seq[i // 2][0],
                        next_pos[1] + inc_seq[i // 2][1])

        return tuple(neighb)


if __name__ == '__main__':
    m = mine_map(grid)
