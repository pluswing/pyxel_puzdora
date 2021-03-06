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
from scene.finish import FinishScene


SCREEN_WIDTH = 33 * 6
BLOCK_MAX_Y = 5
BLOCK_MAX_X = 6
TIME = 10


class App:
    def __init__(self):
        # new Board
        height = math.floor(
            int(SCREEN_WIDTH / BLOCK_MAX_X) * BLOCK_MAX_Y)
        height += 32
        pyxel.init(SCREEN_WIDTH, height)
        pyxel.mouse(True)

        Block.BLOCK_SIZE = 33

        self.initGame()

        pyxel.load("puzdora.pyxel")

        notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
                 'F#', 'G', 'G#', 'A', 'A#', 'B']

        comboNotes = [n + '3' for n in notes[4:]] + \
            [n + '4' for n in notes]

        for i, note in enumerate(comboNotes):
            pyxel.sound(i).set(note, "T", "6", "F", 20)

        pyxel.sound(20).set("C2C1", "TT", "2", "VV", 2)

        pyxel.run(self.update, self.draw)

    def initGame(self):
        self.board = Board(BLOCK_MAX_X, BLOCK_MAX_Y)
        self.scene = MoveBlockScene(self, self.board)
        self.comboCounter = 0
        self.score = 0
        self.life = TIME * 30
        self.maxLife = self.life

    def update(self):
        ret = self.scene.update()
        if ret:
            self.score += ret
            self.comboCounter += 1
        if isinstance(self.scene, MoveBlockScene):
            if self.life < 0:
                self.changeScene(FinishScene(self, self.board))
                return
            if self.scene.draggingBlock:
                self.life -= 1
                if self.life < 0:
                    self.scene.finish = True

    def draw(self):
        self.scene.draw()
        pyxel.text(5, 5,  "SCORE:{}".format(self.score), 7)
        pyxel.text(5, 15, "COMBO:{}".format(self.comboCounter), 7)
        w = SCREEN_WIDTH / self.maxLife * self.life
        color = 11
        if self.life < self.maxLife / 2:
            color = 9
        if self.life < self.maxLife / 8:
            color = 8
        pyxel.rect(0, 28, w, 29, color)

    def nextScene(self, scene):
        if isinstance(scene, MoveBlockScene):
            self.changeScene(EvaluateScene(self, self.board))
        elif isinstance(scene, EvaluateScene):
            if len(scene.chains):
                self.changeScene(ChainScene(self, self.board,
                                            scene.chains, self.comboCounter))
            else:
                self.changeScene(MoveBlockScene(self, self.board))
                self.comboCounter = 0
        elif isinstance(scene, ChainScene):
            self.changeScene(WaitAnimation(DropDownScene(self, self.board)))
        elif isinstance(scene, DropDownScene):
            self.changeScene(FillScene(self, self.board))
        elif isinstance(scene, FillScene):
            self.changeScene(EvaluateScene(self, self.board))

    def changeScene(self, newScene):
        self.scene = newScene


App()
