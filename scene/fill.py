
from .base import GameSceneBase
from block import Block


class FillScene(GameSceneBase):
    def __init__(self, root, block):
        super().__init__(root, block)

    def fillBlocks(self):
        maxDown = self.findMaxDown()
        self.fill(maxDown)

    def findMaxDown(self):
        maxDown = 0
        for x in range(self.board.width):
            down = 0
            for y in range(self.board.height):
                if self.board[y][x].color is None:
                    down += 1
                else:
                    break
            if maxDown < down:
                maxDown = down
        return maxDown

    def fill(self, maxDown):
        for y, line in enumerate(self.board):
            for x, b in enumerate(line):
                if b.color is None:
                    y = b.y
                    b.y -= maxDown * Block.BLOCK_SIZE
                    b.color = Block.randomColor()
                    b.moveTo(b.x, y)

    def update(self):
        super().update()
        self.fillBlocks()
        self.root.nextScene(self)

    def draw(self):
        super().draw()
        self.drawBoard()
