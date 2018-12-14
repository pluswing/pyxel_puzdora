import pyxel
import math
import random
from block import Block


class App:
    SCREEN_WIDTH = 250
    BLOCK_MAX_Y = 5
    BLOCK_MAX_X = 6
    COLOR_MAP = [None, 8, 9, 11, 2, 12, 14]

    def __init__(self):
        self.blockSize = int(self.SCREEN_WIDTH / self.BLOCK_MAX_X)
        self.board = []
        self.initBoard()
        pyxel.init(self.SCREEN_WIDTH, math.floor(
            self.blockSize * self.BLOCK_MAX_Y))
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def initBoard(self):
        r = self.blockSize / 2
        size = self.blockSize
        for y in range(self.BLOCK_MAX_Y):
            line = []
            for x in range(self.BLOCK_MAX_X):
                colorIndex = random.randint(1, len(self.COLOR_MAP) - 1)
                color = self.COLOR_MAP[colorIndex]
                block = Block(x * size + r, y * size + r, r, color)
                line.append(block)
            self.board.append(line)

        self.board[0][5].moveTo(self.board[2][2].x, self.board[2][2].y)

    def update(self):
        # print(pyxel.btn(pyxel.MOUSE_LEFT_BUTTON))
        for line in self.board:
            for b in line:
                b.update()

    def draw(self):
        pyxel.cls(0)
        for line in self.board:
            for b in line:
                b.draw()


App()
