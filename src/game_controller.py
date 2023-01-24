from src.screen import Camera, Screen, TerminalScreen
from src.stage.stage import Grid, Stage
from src.actor.player import Player


class GameController:
    def __init__(self):
        self.screen: Screen = TerminalScreen()
        self.stage: Grid = Stage(width=50, height=40)
        self.camera: Camera = Camera(grid=self.stage, screen=self.screen)
        self.player = None


    def run(self):
        while True:
            self.screen.start_drawing()
            self.camera.draw_grid(2, 5)
            self.screen.finish_drawing()
