import curses


COLORS = [curses.COLOR_BLACK,
          curses.COLOR_RED,
          curses.COLOR_GREEN,
          curses.COLOR_YELLOW,
          curses.COLOR_BLUE,
          curses.COLOR_MAGENTA,
          curses.COLOR_CYAN,
          curses.COLOR_WHITE]
NUM_OF_COLORS = len(COLORS)

def init_color():
    for i in range(NUM_OF_COLORS):
        for j in range(NUM_OF_COLORS):
            curses.init_pair(i * NUM_OF_COLORS + j + 1, COLORS[i], COLORS[j])


def get_pair_id(fore: int, back: int) -> int:
    return fore * NUM_OF_COLORS + back + 1


def change_fore(pair_id: int, fore: int) -> int:
    return fore * NUM_OF_COLORS + (pair_id - 1) % NUM_OF_COLORS + 1


def change_back(pair_id: int, back: int) -> int:
    return (pair_id - 1) // NUM_OF_COLORS * NUM_OF_COLORS + back + 1
