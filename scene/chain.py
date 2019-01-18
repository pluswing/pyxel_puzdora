import pyxel
from .base import GameSceneBase


class ChainScene(GameSceneBase):

    def __init__(self, root, board, chains, chainCounter):
        super().__init__(root, board)
        self.chains = chains
        self.chainCounter = chainCounter

    def update(self):
        super().update()
        if self.board.doneAnimation():
            if len(self.chains):
                chain = self.chains.pop(0)
                for pos in chain:
                    self.board[pos.y][pos.x].blink()
                pyxel.play(0, [self.chainCounter])
                self.chainCounter += 1
            else:
                self.root.nextScene(self)

    def draw(self):
        super().draw()
        self.drawBoard()
