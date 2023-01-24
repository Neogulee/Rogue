import copy
import logging
import os
import sys
import unittest
from typing import List, Type

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.core.grid_vector import GridVector
from src.actor.actor import Actor
from src.actor.character import Character
from src.core.sprite import Sprite
from src.stage.stage import Grid, Square, SquareTag, Stage


class StageTester(unittest.TestCase):
    def setUp(self):
        self.pos: GridVector = GridVector(2, 3)
        self.character: Character = Character(
            pos=self.pos,
            sprite=Sprite("@"),
            max_hp=10,
            power=7,
        )
        
    def test_append_actor(self):
        grid: Grid = Stage(width=7, height=8)
        grid.append_actor(self.character)

        self.assertEqual(grid[self.pos].get_actor(SquareTag.CHARACTER), self.character)
        
    def test_remove_actor(self):
        grid: Grid = Stage(width=7, height=8)
        grid.append_actor(self.character)
        grid.remove_actor(self.character)
        self.assertEqual(grid[self.pos].get_actor(SquareTag.CHARACTER), None)

    def test_getitem(self):
        log = logging.getLogger("StageTester")
        
        grid: Grid = Stage(width=7, height=8)
        arr: List[List[Square]] = grid[:]
        grid.append_actor(self.character)
        string = "\n"
        for row in grid[:]:
            for item in row:
                string += str(item.get_actor(SquareTag.CHARACTER)) + " "
            string += "\n"
        log.debug(string)
        
        for y in range(8):
            for x in range(7):
                if y == self.pos.y and x == self.pos.x:
                    continue
                self.assertEqual(arr[y][x].get_actor(SquareTag.CHARACTER), None)
        self.assertEqual(arr[self.pos.y][self.pos.x].get_actor(SquareTag.CHARACTER), self.character)
        
        
    def test_property(self):
        grid: Grid = Stage(width=7, height=8)
        self.assertEqual(7, grid.width)
        self.assertEqual(8, grid.height)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("StageTester").setLevel(logging.DEBUG)
    unittest.main()