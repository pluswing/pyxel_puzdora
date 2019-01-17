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


SCREEN_WIDTH = 33 * 6
BLOCK_MAX_Y = 5
BLOCK_MAX_X = 6


class App:
    def __init__(self):
        # new Board
        height = math.floor(
            int(SCREEN_WIDTH / BLOCK_MAX_X) * BLOCK_MAX_Y)
        height += 32
        pyxel.init(SCREEN_WIDTH, height)
        pyxel.mouse(True)

        Block.BLOCK_SIZE = 33
        self.board = Board(BLOCK_MAX_X, BLOCK_MAX_Y)
        self.scene = MoveBlockScene(self, self.board)

        pyxel.load("puzdora.pyxel")
        pyxel.sound(0).set("e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
                           "p",
                           "6",
                           "vffn fnff vffs vfnn",
                           25,)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.scene.update()
        if pyxel.btnp(pyxel.KEY_1):
            pyxel.play(0, [0, 1], loop=True)

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
