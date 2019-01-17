import pyxel
import math
import random


class Block:
    BLOCK_SIZE = 0
    WHITE = 7

    def __init__(self, x, y, color):
        self.x = int(x)
        self.y = int(y)
        self.r = 16
        self.color = color
        self.targetX = self.x
        self.targetY = self.y
        self.animation = False
        self.animationFrame = 0
        self.animationDuration = 4
        self.mx = 0
        self.my = 0

        self.originalColor = color
        self.blinkCounter = 0

    def update(self):
        if self.blinkCounter > 0:
            if self.color == self.WHITE:
                self.color = self.originalColor
                self.blinkCounter -= 1
                if self.blinkCounter <= 0:
                    self.blinkCounter = 0
                    self.color = None
            else:
                self.color = self.WHITE
            return

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

        pyxel.blt(self.x-self.r, self.y-self.r, 0, 0, (self.r*2)
                  * (self.color-1), self.r*2, self.r*2, 0)

    def moveToWithDuration(self, x, y, duration=4):
        self.targetX = int(x)
        self.targetY = int(y)
        self.animation = True
        self.mx = (self.targetX - self.x) / duration
        self.my = (self.targetY - self.y) / duration
        self.animationFrame = 0
        self.animationDuration = duration

    def moveTo(self, x, y):
        diffX = self.x - x
        diffY = self.y - y
        l = math.sqrt(diffX * diffX + diffY * diffY)
        duration = int(l / (self.r / 2))
        if duration < 1:
            duration = 1
        self.moveToWithDuration(x, y, duration)

    def blink(self, count=5):
        self.blinkCounter = count
        self.animation = True
        self.mx = 0
        self.my = 0
        self.animationFrame = 0
        self.animationDuration = 4

    @classmethod
    def _create(self, x, y, color):
        size = self.BLOCK_SIZE
        ox, oy = self.calcPos(x, y)
        return Block(ox, oy, color)

    @classmethod
    def create(self, x, y):
        return self._create(x, y, self.randomColor())

    @classmethod
    def createWithoutColor(self, x, y):
        return self._create(x, y, None)

    @classmethod
    def randomColor(self):
        return random.randint(1, 6)

    @classmethod
    def calcPos(self, x, y):
        size = self.BLOCK_SIZE
        return x * size + size / 2, y * size + size / 2 + 32
