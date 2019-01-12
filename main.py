import pyxel
import math
from block import Block
from board import Board

from scene.move_block import MoveBlockScene
from scene.evaluate import EvaluateScene
from scene.chain import ChainScene
from scene.drop_down import DropDownScene
from scene.fill import FillScene
from scene.wait import WaitAnimation


SCREEN_WIDTH = 250
BLOCK_MAX_Y = 5
BLOCK_MAX_X = 6


class App:
    def __init__(self):
        # new Board
        pyxel.init(SCREEN_WIDTH, math.floor(
            int(SCREEN_WIDTH / BLOCK_MAX_X) * BLOCK_MAX_Y))
        pyxel.mouse(True)

        Block.BLOCK_SIZE = int(SCREEN_WIDTH / BLOCK_MAX_X)
        self.board = Board(BLOCK_MAX_X, BLOCK_MAX_Y)
        self.scene = MoveBlockScene(self, self.board)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.scene.update()

    def draw(self):
        self.scene.draw()

    def nextScene(self, scene):
        if isinstance(scene, MoveBlockScene):
            self.changeScene(EvaluateScene(self, self.board))
        elif isinstance(scene, EvaluateScene):
            if len(scene.chains):
                self.changeScene(ChainScene(self, self.board, scene.chains))
            else:
                self.changeScene(MoveBlockScene(self, self.board))
        elif isinstance(scene, ChainScene):
            self.changeScene(WaitAnimation(DropDownScene(self, self.board)))
        elif isinstance(scene, DropDownScene):
            self.changeScene(FillScene(self, self.board))
        elif isinstance(scene, FillScene):
            self.changeScene(EvaluateScene(self, self.board))

    def changeScene(self, newScene):
        self.scene = newScene


App()
