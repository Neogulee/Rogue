from abc import ABCMeta, abstractmethod
from typing import List

from .actor import Actor
from src.core.sprite import Sprite
from src.core.grid_vector import GridVector


class HpSystemListener(metaclass=ABCMeta):
    def on_max_hp_changed(self, transform_id: int, old: int, new: int) -> None:
        pass
        
    def on_hp_changed(self, transform_id: int, old: int, new: int) -> None:
        pass


class HpSystem(metaclass=ABCMeta):
    @abstractmethod
    def append_hp_system_listener(self, listener: HpSystemListener) -> bool:
        pass

    @abstractmethod
    def remove_hp_system_listener(self, listener: HpSystemListener) -> bool:
        pass
        
    @property
    @abstractmethod
    def max_hp(self) -> int:
        pass
        
    @max_hp.setter
    @abstractmethod
    def max_hp(self, value: int):
        pass

    @property
    @abstractmethod
    def hp(self) -> int:
        pass
        
    @hp.setter
    @abstractmethod
    def hp(self, value: int):
        pass


class Attacker(metaclass=ABCMeta):
    @abstractmethod
    def attack(self, target: HpSystem) -> None:
        pass
        
        
class Character(Actor, Attacker, HpSystem):
    def __init__(self,
            pos: GridVector,
            sprite: Sprite,
            max_hp: int,
            power: int):
        super().__init__(pos=pos, sprite=sprite)
        self.__max_hp = max_hp
        self.__hp = self.__max_hp
        self.__power = power
        self.__listener_list: List[HpSystemListener] = []

    def attack(self, target: HpSystem) -> None:
        target.hp -= self.__power
        
    def append_hp_system_listener(self, listener: HpSystemListener) -> bool:
        if listener not in self.___listener_list:
            self.__listener_list.append(listener)
            return True
        return False

    def remove_hp_system_listener(self, listener: HpSystemListener) -> bool:
        if listener in self.___listener_list:
            self.__listener_list.remove(listener)
            return True
        return False

    def __notify_max_hp_changed(self, old: int) -> None:
        for listener in self.__listener_list:
            listener.on_max_hp_changed(self.transform_id, old, self.__max_hp)

    def __notify_hp_changed(self, old: int) -> None:
        for listener in self.__listener_list:
            listener.on_hp_changed(self.transform_id, old, self.__hp)
        
    @property
    def max_hp(self) -> int:
        return self.__max_hp
        
    @max_hp.setter
    def max_hp(self, value: int):
        value = max(0, value)
        old = self.__max_hp
        self.__max_hp = value
        if self.__hp > self.__max_hp:
            self.hp = self.__max_hp
        self.__notify_max_hp_changed(old)        

    @property
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, value: int):
        value = max(0, value)
        old = self.__hp
        self.__hp = value
        self.__notify_hp_changed(old)
        if self.__hp == 0:
            self.destroy()

    @property
    def power(self) -> int:
        return self.__power


class GeneralCharacter(Character):
    pass