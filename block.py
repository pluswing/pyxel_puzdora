import pyxel
import math
import random


class Block:
    COLOR_MAP = [None, 8, 9, 11, 2, 12, 14]
    BLOCK_SIZE = 0

    def __init__(self, x, y, r, color):
        self.x = int(x)
        self.y = int(y)
        self.r = r
        self.color = color

        self.targetX = self.x
        self.targetY = self.y
        self.animation = False
        self.animationFrame = 0
        self.animationDuration = 4
        self.mx = 0
        self.my = 0

    def update(self):
        if self.animation:
            self.x += self.mx
            self.y += self.my
            self.animationFrame += 1
            if self.animationFrame == self.animationDuration:
                self.x = self.targetX
                self.y = self.targetY
                self.animation = False

    def isHit(self, mouseX, mouseY):
        diffX = mouseX - self.x
        diffY = mouseY - self.y
        l = math.sqrt(diffX * diffX + diffY * diffY)
        return l < self.r

    def draw(self):
        if self.color is None:
            return
        pyxel.circ(self.x, self.y, self.r, self.COLOR_MAP[self.color])

    def moveTo(self, x, y):
        self.targetX = int(x)
        self.targetY = int(y)
        self.animation = True
        self.mx = (self.targetX - self.x) / self.animationDuration
        self.my = (self.targetY - self.y) / self.animationDuration
        self.animationFrame = 0

    @classmethod
    def _createBlock(self, x, y, color):
        r = self.BLOCK_SIZE / 2
        size = self.BLOCK_SIZE
        ox, oy = self.calcBlockPos(x, y)
        return Block(ox, oy, r, color)

    @classmethod
    def createBlock(self, x, y):
        return self._createBlock(x, y, self.randomColor())

    @classmethod
    def createBlockWithoutColor(self, x, y):
        return self._createBlock(x, y, None)

    @classmethod
    def randomColor(self):
        return random.randint(1, len(self.COLOR_MAP) - 1)

    @classmethod
    def calcBlockPos(self, x, y):
        size = self.BLOCK_SIZE
        return x * size + size / 2, y * size + size / 2
