import pyxel
from .base import GameSceneBase


class ChainScene(GameSceneBase):
    def __init__(self, root, board, chains):
        super(ChainScene, self).__init__(root, board)
        self.chains = chains

    def update(self):
        super(ChainScene, self).update()
        if self.board.doneAnimation():
            if len(self.chains):
                chain = self.chains.pop(0)
                for pos in chain:
                    self.board[pos.y][pos.x].color = None
                    self.board[pos.y][pos.x].fadeOut()
            else:
                self.root.nextScene(self)

    def draw(self):
        super(ChainScene, self).draw()
        self.drawBoard()
