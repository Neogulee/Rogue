import logging
import os
import sys
import unittest
from typing import Type

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.actor.character import Character
from src.core.grid_vector import GridVector
from src.core.sprite import Sprite
from src.screen import Camera, Screen
from src.stage.stage import Grid, Square, SquareTag, Stage


class TestScreen(Screen):
    def __init__(self):
        self.arr = [[None] * 100 for _ in range(100)]
        
    def close(self) -> None:
        pass
        
    def get_key(self) -> str:
        pass
    
    def start_drawing(self) -> None:
        pass
    
    def finish_drawing(self) -> None:
        pass

    def draw(self, x: int, y: int, sprite: Sprite) -> None:
        self.arr[y][x] = sprite

    def draw_overlay(self, x: int, y: int, back: int) -> None:
        pass


class TestStage(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)

    def fill_character(self, ch = "#") -> None:
        for y in range(self.height):
            for x in range(self.width):
                self[GridVector(x=x, y=y)].character = Character(
                    pos=GridVector(x=x, y=y),
                    sprite = Sprite(ch),
                    max_hp=10,
                    power=3
                )


class CameraTester(unittest.TestCase):
    def test_property(self):
        camera = Camera(Stage(30, 20), TestScreen())
        self.assertEqual(camera.sight, 8)
        self.assertEqual(camera.size, 17)
        
        camera.sight = 6
        self.assertEqual(camera.sight, 6)
        self.assertEqual(camera.size, 13)
        
        camera.sight = -1
        self.assertEqual(camera.sight, 0)
        self.assertEqual(camera.size, 1)
        
    def test_reset_sight(self):
        camera = Camera(Stage(30, 20), TestScreen())
        camera.sight = 6
        camera.reset_sight()
        self.assertEqual(camera.sight, 8)

    def test_get_viewport(self):
        stage = TestStage(30, 20)
        stage.fill_character()

        camera = Camera(stage, TestScreen())
        camera.sight = 2
        view_port = camera.get_viewport(x=0, y=1)
        height = len(view_port)
        width = len(view_port[0])
        self.assertEqual(height, 4)
        self.assertEqual(width, 3)
        for y in range(height):
            for x in range(width):
                self.assertEqual(type(view_port[y][x]), Square)


    def test_draw_grid(self):
        log = logging.getLogger("ScreenTester")
        
        stage = TestStage(30, 20)
        stage.fill_character("#")
        screen = TestScreen()
        
        camera = Camera(stage, screen)
        camera.sight = 2

        pos = GridVector(x=2, y=3)
        character = Character(
            pos=pos,
            sprite=Sprite("@"),
            max_hp = 20,
            power = 10
        )
        square: Square = stage[pos]
        square.remove(SquareTag.CHARACTER)     
        stage.append_actor(character)

        camera.draw_grid(x=1, y=3)
                
        for y in range(10):
            for x in range(10):
                # log.debug("y={}, x={}, {}".format(y, x, screen.arr[y][x]))
                if 1 <= x and x <= 4 and y <= 4:
                    self.assertIsNot(screen.arr[y][x], None)
                else:
                    self.assertIs(screen.arr[y][x], None)
        self.assertEqual(screen.arr[2][3].ch, "@")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("ScreenTester").setLevel(logging.DEBUG)
    unittest.main()
