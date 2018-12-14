import pyxel


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
        self.animationDuration = 20
        self.mx = 0
        self.my = 0

    def needAnimation(self):
        return self.targetX != self.x or self.targetY != self.y

    def update(self):
        if self.animation:
            self.x += self.mx
            self.y += self.my
            self.animationFrame += 1
            if self.animationFrame == self.animationDuration:
                self.x = self.targetX
                self.y = self.targetY
                self.animation = False
            return

        if self.needAnimation():
            self.animation = True
            self.mx = (self.targetX - self.x) / self.animationDuration
            self.my = (self.targetY - self.y) / self.animationDuration
            self.animationFrame = 0

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, self.color)

    def moveTo(self, x, y):
        self.targetX = int(x)
        self.targetY = int(y)
