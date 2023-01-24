import os
import sys
from typing import Dict, List, Type
from xml.etree.ElementTree import ElementTree, parse

from .character import Character, GeneralCharacter
from src.core.grid_vector import GridVector
from src.core.utils import DEFS_DIR
from src.core.sprite import Sprite


class CharacterFactory:
    __character_dict: Dict[str, ElementTree] = dict()
    
    def __init__(self):
        if not self.__character_dict:
            self.__init_dict(DEFS_DIR)

    def __init_dict(self, root: str):
        list_dir: List[str] = os.listdir(root)
        for dir in list_dir:
            path = os.path.join(root, dir)
            if os.path.isdir(path):
                self.__init_dict(path)
            else:
                try:
                    tree: ElementTree = parse(path)
                    characters = tree.findall("CharacterDef")
                    for character in characters:
                        self.__character_dict[character.find("defName").text] = character
                except:
                    pass
                
     # add exception
    def create(self, def_name:str, pos: GridVector) -> Character:
        tree: ElementTree = self.__character_dict[def_name]

        cls: Type[Character] = getattr(sys.modules[__name__], tree.find("class").text)
        sprite_tree: ElementTree = tree.find("sprite")
        sprite: Sprite = Sprite(sprite_tree.find("ch").text)
        character: Character = cls(
            pos=pos,
            sprite=sprite,
            max_hp=int(tree.find("hp").text),
            power=int(tree.find("power").text),
        );    
        return character
        
        
 
    