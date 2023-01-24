from abc import ABCMeta, abstractmethod
from typing import List

from src.core.grid_vector import GridVector
from src.core.sprite import Sprite


class TransformListener(metaclass=ABCMeta):
    def on_pos_changed(self, transform_id: int, old: GridVector, new: GridVector) -> None:
        pass

    def on_destroyed(self, transform_id: int) -> None:
        pass


class Transform(metaclass=ABCMeta):
    @abstractmethod
    def destroy(self) -> None:
        pass

    @abstractmethod
    def append_transform_listener(self, listener: TransformListener) -> bool:
        pass

    @abstractmethod
    def remove_transform_listener(self, listener: TransformListener) -> bool:
        pass
    
    @property
    @abstractmethod
    def pos(self) -> GridVector:
        pass

    @pos.setter
    @abstractmethod
    def pos(self, value: GridVector):
        pass

    @property
    @abstractmethod
    def sprite(self) -> Sprite:
        pass
        
    @property
    @abstractmethod
    def is_destroyed(self) -> bool:
        pass

    @property
    def transform_id(self) -> int:
        pass
    
    
class Actor(Transform):
    __global_transform_id: int = 0
    
    def __init__(self, pos: GridVector, sprite: Sprite):
        self.__pos: GridVector = pos
        self.__is_destroyed: bool = False
        self.__listener_list: List[TransformListener] = []
        self.__transform_id: int = self.__global_transform_id
        self.__global_transform_id += 1
        self.__sprite = sprite

    def destroy(self) -> None:
        self.__is_destroyed = True
        self.__notify_destroyed()

    def append_transform_listener(self, listener: TransformListener) -> bool:
        if listener not in self.__listener_list:
            self.__listener_list.append(listener)
            return True
        return False

    def remove_transform_listener(self, listener: TransformListener) -> bool:
        if listener in self.__listener_list:
            self.__listener_list.remove(listener)
            return True
        return False

    def __notify_destroyed(self) -> None:
        for listener in self.__listener_list:
            listener.on_destroyed(self.__transform_id)

    def __notify_pos_changed(self, old: GridVector) -> None:
        for listener in self.__listener_list:
            listener.on_pos_changed(self.__transform_id, old, self.__pos)

    def __repr__(self) -> str:
        return "Actor(x={}, y={})".format(self.pos.x, self.pos.y)
        
    @property
    def pos(self) -> GridVector:
        return self.__pos.copy()

    @pos.setter
    def pos(self, value: GridVector):
        old = self.__pos
        self.__pos = value
        self.__notify_pos_changed(old, self.__pos)

    @property
    def sprite(self) -> Sprite:
        return self.__sprite
        
    @property
    def is_destroyed(self) -> bool:
        return self.__is_destroyed

    @property
    def transform_id(self) -> int:
        return self.__transform_id
