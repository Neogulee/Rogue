from __future__ import annotations

import curses

from src.core.color import get_pair_id


class Sprite:
    def __init__(self, ch: str,
            fore: int=curses.COLOR_WHITE,
            back: str=curses.COLOR_BLACK):
        if len(ch) != 1:
            raise "ch size must be 1"
            
        self.__ch: str = ch
        self.__fore: str = fore
        self.__back: str = back

    @property
    def fore(self) -> int:
        return self.__fore

    @property
    def back(self) -> int:
        return self.__back

    @property
    def pair_id(self) -> int:
        return get_pair_id(fore=self.__fore, back=self.__back)
        
    @property
    def ch(self) -> str:
        return self.__ch

    def __eq__(self, other: Sprite) -> bool:
        return self.__ch == other.__ch\
                and self.__fore == other.__fore\
                and self.__back == other.__back
        
    def __repr__(self) -> str:
        return "Sprite(%s, %s, %s)"%(self.__ch, self.__fore, self.__back)


SPACE_SPRITE: Sprite = Sprite(" ")
NEW_LINE_SPRITE: Sprite = Sprite("\n")