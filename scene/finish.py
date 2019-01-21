
from .base import GameSceneBase
from block import Block
import pyxel


class FinishScene(GameSceneBase):
    def __init__(self, root, block):
        super().__init__(root, block)
        self.color = 0

    def update(self):
        super().update()
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.root.initGame()

        self.color += 1
        if self.color > 15:
            self.color = 1

    def draw(self):
        super().draw()
        self.drawBoard()
        pyxel.text(80, 100, "FINISH", self.color)
        pyxel.text(52, 120, "PUSH SPACE TO NEXT GAME", self.color)
