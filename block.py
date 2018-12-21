import pyxel
import math


class Block:
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
        pyxel.circ(self.x, self.y, self.r, self.color)

    def moveTo(self, x, y):
        self.targetX = int(x)
        self.targetY = int(y)
        self.animation = True
        self.mx = (self.targetX - self.x) / self.animationDuration
        self.my = (self.targetY - self.y) / self.animationDuration
        self.animationFrame = 0
