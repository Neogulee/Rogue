import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.actor.character import Character
from src.actor.character_factory import CharacterFactory
from src.core.grid_vector import GridVector
from src.core.sprite import Sprite


class CharacterFactoryTester(unittest.TestCase):
    def test_create(self):
        factory = CharacterFactory()
        pos = GridVector(2, 3)
        
        slime: Character = factory.create("Slime", pos)
        self.assertEqual(slime.pos, pos)
        self.assertEqual(slime.max_hp, 10)
        self.assertEqual(slime.power, 3)
        self.assertEqual(slime.sprite, Sprite("S"))


if __name__ == "__main__":
    unittest.main()