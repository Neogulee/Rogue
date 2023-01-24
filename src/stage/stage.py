from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List, Tuple, Union

from src.actor.character import Character
from src.actor.actor import Actor, TransformListener
from src.core.grid_vector import GridVector


class SquareTag(Enum):
    CHARACTER = 0
        
    
class Square:
    def __init__(self):
        self.character: Character = None

    def get_tag(self, actor: Actor) -> SquareTag:
        if isinstance(actor, Character):
            return SquareTag.CHARACTER
        
    def find_tag(self, transform_id: int) -> SquareTag:
        if self.character.transform_id == transform_id:
            return SquareTag.CHARACTER
        return None
        
    def get_actor(self, tag: SquareTag) -> Actor:
        if tag == SquareTag.CHARACTER:
            return self.character
        return None
        
    def set_actor(self, actor: Actor) -> None:    
        tag = self.get_tag(actor)
        if tag == SquareTag.CHARACTER:
            self.character = actor

    def remove(self, tag: SquareTag) -> None:
        if tag == SquareTag.CHARACTER:
            self.character = None

        
class Grid(metaclass=ABCMeta):
    @abstractmethod
    def append_actor(self, actor: Actor) -> None:
        pass
        
    @abstractmethod
    def remove_actor(self, actor: Actor) -> None:
        pass
    
    @abstractmethod
    def __getitem__(self, idx: Union[GridVector, slice]) -> Union[Square, List[List[Square]]]:
        pass

    # @abstractmethod
    # def __setitem__(self, idx: Union[GridVector, slice],
    #         item: Union[Square, List[List[Square]]]):
    #     pass

    @property
    @abstractmethod    
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass
    

class Stage(Grid, TransformListener):
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__square_list: List[Square] = [[Square() for _ in range(width)] for _ in range(height)]

    def __get_idx(self, slice) -> Tuple[int, int, int, int]:
            start = slice.start
            stop = slice.stop
            
            start_x = start.x if start is not None else None
            start_y = start.y if start is not None else None
            stop_x = stop.x if stop is not None else None
            stop_y = stop.y if stop is not None else None
        
            return start_x, start_y, stop_x, stop_y

    def append_actor(self, actor: Actor) -> None:
        self[actor.pos].set_actor(actor)
        # append listener
        
    def remove_actor(self, actor: Actor) -> None:
        square = self[actor.pos]
        square.remove(square.find_tag(actor.transform_id))
        
    def __getitem__(self, idx: Union[GridVector, slice]) -> Union[Square, List[List[Square]]]:
        if isinstance(idx, slice):
            start_x, start_y, stop_x, stop_y = self.__get_idx(idx)
            
            return [row[start_x:stop_x:idx.step]
                for row in self.__square_list[start_y:stop_y:idx.step]]
        return self.__square_list[idx.y][idx.x]

    # def __setitem__(self, idx: Union[GridVector, slice],
    #         item: Union[Square, List[List[Square]]]):
    #     if isinstance(idx, slice):
    #         start_x, start_y, stop_x, stop_y = self.__get_idx(idx)
            
    #         rows = self.__square_list[start_y:stop_y]
    #         for i, row in enumerate(rows):
    #             row[start_x:stop_x] = item[i]
    #     else:
    #         self.__square_list[idx.y][idx.x] = item

    def move_actor(self, transform_id: int, src: GridVector, dest: GridVector) -> bool:
        src_square = self.__square_list[src]
        dest_square = self.__square_list[dest]
        tag = src_square.find_tag(transform_id)
        if tag is None or dest_square.get_actor(tag) is not None:
            return False
            
        actor = src_square.get_actor(tag)
        src_square.remove_actor(tag)
        dest_square.set_actor(tag, actor)
        return True
        
        
    def on_pos_changed(self, transform_id: int, old: GridVector, new: GridVector) -> None:
        self.move_actor(transform_id, old, new)

    def on_destroyed(self, transform_id: int) -> None:
        pass
    
    @property
    def width(self) -> int:
        return self.__width
        
    @property
    def height(self) -> int:
        return self.__height        
    