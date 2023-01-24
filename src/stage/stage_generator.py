from abc import ABCMeta, abstractmethod

from src.stage.stage import Stage


class StageGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate() -> Stage:
        pass


class TestStageGenerator(StageGenerator):
    def generate() -> Stage:
        
    