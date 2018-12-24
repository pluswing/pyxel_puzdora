import pyxel
from .base import GameSceneBase


class ChainScene(GameSceneBase):
    def __init__(self, root, board, chains):
        super(ChainScene, self).__init__(root, board)
        self.chains = chains

    def update(self):
        super(ChainScene, self).update()
        for chain in self.chains:
            for pos in chain:
                self.board[pos.y][pos.x].color = None

        self.root.nextScene(self)

    def draw(self):
        super(ChainScene, self).draw()
        self.drawBoard()
