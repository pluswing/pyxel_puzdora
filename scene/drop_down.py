import pyxel
from .base import GameSceneBase
from block import Block


class DropDownScene(GameSceneBase):
    def __init__(self, root, block):
        super().__init__(root, block)

    def dropDown(self):
        for y in reversed(range(self.board.height)):
            for x in range(self.board.width):
                if self.board[y][x].color is None:
                    upper = self.getUpperBlock(x, y)
                    if upper:
                        ux, uy = self.board.getBlockPos(upper)
                        self.board[uy][ux] = Block.createWithoutColor(
                            ux, uy)
                        self.board[y][x] = upper
                        ox, oy = Block.calcPos(x, y)
                        upper.moveTo(ox, oy)

    def getUpperBlock(self, x, y):
        for y in reversed(range(y)):
            if self.board[y][x].color:
                return self.board[y][x]
        return None

        # FIXME

    def update(self):
        super().update()
        self.dropDown()
        self.root.nextScene(self)

    def draw(self):
        super().draw()
        self.drawBoard()
