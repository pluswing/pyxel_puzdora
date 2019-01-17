import pyxel
from .base import GameSceneBase


class ChainScene(GameSceneBase):

    def __init__(self, root, board, chains):
        super().__init__(root, board)
        self.chains = chains

    def update(self):
        super().update()
        if self.board.doneAnimation():
            if len(self.chains):
                chain = self.chains.pop(0)
                for pos in chain:
                    self.board[pos.y][pos.x].blink()
            else:
                self.root.nextScene(self)

    def draw(self):
        super().draw()
        self.drawBoard()
