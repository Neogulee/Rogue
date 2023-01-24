from __future__ import annotations

from abc import ABCMeta, abstractmethod
import curses
from typing import List


from src.actor.actor import Transform
from src.core.color import init_color
from src.core.sprite import Sprite, SPACE_SPRITE
from src.core.grid_vector import GridVector
from src.stage.stage import Grid, Square


class Camera:
    __DEFAULT_SIGHT: int = 8

    def __init__(self, grid: Grid, screen: Screen):
        self.grid: Grid = grid
        self.screen: Screen = screen
        self.__sight: int = self.__DEFAULT_SIGHT
    
    def reset_sight(self) -> None:
        self.__sight = self.__DEFAULT_SIGHT

    def get_viewport(self, x: int, y: int) -> List[List[Square]]:
        top = max(0, y - self.__sight)
        bottom = min(self.grid.height, y + self.__sight + 1)
        left = max(0, x - self.__sight)
        right = min(self.grid.width, x + self.__sight + 1)

        a = GridVector(left, top)
        b = GridVector(right, bottom)
        return self.grid[a:b]

    def draw_grid(self, x: int, y: int):
        viewport = self.get_viewport(x, y)
        top = self.size - len(viewport)
        left = self.size - len(viewport[0]) if len(viewport) > 0 else 0
        
        for y, row in enumerate(viewport):
            for x, square in enumerate(row):
                if square is not None and square.character is not None:
                    self.screen.draw(x=left + x, y=top + y, sprite=square.character.sprite)

    @property
    def sight(self) -> int:
        return self.__sight
    
    @sight.setter
    def sight(self, sight: int):
        self.__sight = 0 if sight < 0 else sight

    @property
    def size(self) -> int:
        return self.__sight * 2 + 1

        
class Screen(metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        pass
        
    @abstractmethod
    def get_key(self) -> str:
        pass
    
    @abstractmethod
    def start_drawing(self) -> None:
        pass
    
    @abstractmethod
    def finish_drawing(self) -> None:
        pass

    @abstractmethod
    def draw(self, x: int, y: int, sprite: Sprite) -> None:
        pass

    @abstractmethod
    def draw_overlay(self, x: int, y: int, back: int) -> None:
        pass


class TerminalScreen(Screen):
    def __init__(self):
        self.__window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        init_color()
        self.__window.keypad(True)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        curses.nocbreak()
        self.__window.keypad(False)
        curses.echo()
        curses.endwin()

    def get_key(self) -> str:
        return self.__window.getkey()

    def start_drawing(self) -> None:
        # self.__window.clear()
        pass

    def finish_drawing(self) -> None:
        self.__window.refresh()
        
    def draw(self, x: int, y: int, sprite: Sprite) -> None:
        self.__window.addstr(y, x, sprite.ch, curses.color_pair(sprite.pair_id))

    def draw_overlay(self, x: int, y: int, back: int) -> None:
        # ch = self.__window.getstr(y, x)
        pass
