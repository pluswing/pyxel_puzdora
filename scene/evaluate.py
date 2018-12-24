import pyxel
from .base import GameSceneBase
from pos import Pos


class EvaluateScene(GameSceneBase):

    def __init__(self, root, board):
        super(EvaluateScene, self).__init__(root, board)
        self.colors = []
        self.eraseBlocks = []
        self.chains = []

    def boardColors(self):
        colors = []
        for line in self.board:
            l = []
            for b in line:
                l.append(b.color)
            colors.append(l)
        return colors

    def initEraseBlocks(self):
        self.eraseBlocks = []
        for y in range(self.board.height):
            self.eraseBlocks.append([0 for x in range(self.board.width)])

    def evaluate(self):
        self.initEraseBlocks()
        self.evaluateX()
        self.evaluateY()
        return self.getChains()

    def evaluateX(self):
        for y in range(self.board.height):
            for x in range(self.board.width - 2):
                b = self.board
                if b[y][x].color == b[y][x+1].color == b[y][x+2].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y][x+1] = b[y][x].color
                    self.eraseBlocks[y][x+2] = b[y][x].color

    def evaluateY(self):
        for y in range(self.board.height - 2):
            for x in range(self.board.width):
                b = self.board
                if b[y][x].color == b[y+1][x].color == b[y+2][x].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y+1][x] = b[y][x].color
                    self.eraseBlocks[y+2][x] = b[y][x].color

    def getChains(self):
        chains = []
        for y in range(self.board.height):
            for x in range(self.board.width):
                posList = self.getChain(x, y, self.eraseBlocks[y][x], [])
                if len(posList):
                    chains.append(posList)
        return chains

    def getChain(self, x, y, color, posList):
        if self.eraseBlocks[y][x] == 0:
            return posList
        if self.eraseBlocks[y][x] != color:
            return posList
        self.eraseBlocks[y][x] = 0

        if x > 0:
            self.getChain(x-1, y, color, posList)
        if x < self.board.width - 1:
            self.getChain(x+1, y, color, posList)
        if y > 0:
            self.getChain(x, y-1, color, posList)
        if y < self.board.height - 1:
            self.getChain(x, y+1, color, posList)

        posList.append(Pos(x, y))
        return posList

    def update(self):
        super(EvaluateScene, self).update()
        self.chains = self.evaluate()
        self.root.nextScene(self)

    def draw(self):
        super(EvaluateScene, self).draw()
        self.drawBoard()
