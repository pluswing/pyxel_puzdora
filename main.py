import pyxel
import math
import random
from block import Block


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return "[x:{}, y:{}]".format(self.x, self.y)


class App:
    SCREEN_WIDTH = 250
    BLOCK_MAX_Y = 5
    BLOCK_MAX_X = 6
    COLOR_MAP = [None, 8, 9, 11, 2, 12, 14]

    def __init__(self):
        self.blockSize = int(self.SCREEN_WIDTH / self.BLOCK_MAX_X)
        self.board = []
        self.initBoard()
        self.hasBlock = None
        self.colors = []
        self.chains = []
        self.state = 0
        self.eraseBlocks = []

        pyxel.init(self.SCREEN_WIDTH, math.floor(
            self.blockSize * self.BLOCK_MAX_Y))
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def initBoard(self):
        for y in range(self.BLOCK_MAX_Y):
            line = []
            for x in range(self.BLOCK_MAX_X):
                line.append(self.createBlock(x, y))
            self.board.append(line)

    def _createBlock(self, x, y, color):
        r = self.blockSize / 2
        size = self.blockSize
        ox, oy = self.getBlockOriginPos(x, y)
        return Block(ox, oy, r, color)

    def createBlock(self, x, y):
        return self._createBlock(x, y, self.randomColor())

    def createBlockWithoutColor(self, x, y):
        return self._createBlock(x, y, None)

    def randomColor(self):
        colorIndex = random.randint(1, len(self.COLOR_MAP) - 1)
        return self.COLOR_MAP[colorIndex]

    def initEraseBlocks(self):
        self.eraseBlocks = []
        for y in range(self.BLOCK_MAX_Y):
            self.eraseBlocks.append([0 for x in range(self.BLOCK_MAX_X)])

    def update(self):
        print(self.state)

        # ブロックのアップデートは必ずやる
        for line in self.board:
            for b in line:
                b.update()

        if self.state == 1:
            if self.doneAnimation():
                self.state = 2
            return

        if self.state == 2:
            # ブロックの削除処理
            for chain in self.chains:
                for pos in chain:
                    self.board[pos.y][pos.x].color = None
            self.state = 3
            self.chains = []
            return

        if self.state == 3:
            if self.doneAnimation():
                self.state = 4
            return

        if self.state == 4:
            # ブロックを詰める処理
            self.dropDownBlocks()
            self.state = 5
            return

        if self.state == 5:
            if self.doneAnimation():
                self.state = 6
            return

        if self.state == 6:
            # ブロックを追加する処理
            self.fillBlocks()
            self.state = 7
            return

        if self.state == 7:
            # 盤面の評価
            self.evaluateBoard()
            if len(self.chains):
                self.state = 1
            else:
                self.state = 0
            return

        # ブロック持つ判定
        for line in self.board:
            for b in line:
                if self.hasBlock is None and pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                    if b.isHit(pyxel.mouse_x, pyxel.mouse_y):
                        self.hasBlock = b
        # ブロックを離す判定
        if self.hasBlock and not pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            self.hasBlock.moveTo(self.hasBlock.targetX, self.hasBlock.targetY)
            self.hasBlock = None
            self.state = 7

        # ブロックの移動
        if self.hasBlock:
            self.hasBlock.x = pyxel.mouse_x
            self.hasBlock.y = pyxel.mouse_y

            # ブロックの入れ替え
            for line in self.board:
                for b in line:
                    if b.isHit(pyxel.mouse_x, pyxel.mouse_y) and not b.animation:
                        if self.hasBlock != b:
                            # 見た目上の位置を入れ替える（アニメーション）
                            tx = b.targetX
                            ty = b.targetY
                            b.moveTo(self.hasBlock.targetX,
                                     self.hasBlock.targetY)
                            self.hasBlock.targetX = tx
                            self.hasBlock.targetY = ty
                            # board上の位置を入れ替える。
                            x1, y1 = self.getBlockPos(self.hasBlock)
                            x2, y2 = self.getBlockPos(b)
                            self.board[y1][x1] = b
                            self.board[y2][x2] = self.hasBlock

    def doneAnimation(self):
        for line in self.board:
            for b in line:
                if b.animation:
                    return False
        return True

    def fillBlocks(self):
        maxDown = self.findMaxDown()
        self.fill(maxDown)

    def findMaxDown(self):
        maxDown = 0
        for x in range(self.BLOCK_MAX_X):
            down = 0
            for y in range(self.BLOCK_MAX_Y):
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
                    b.y -= maxDown * self.blockSize
                    b.color = self.randomColor()
                    b.moveTo(b.x, y)

    def dropDownBlocks(self):
        for y in reversed(range(self.BLOCK_MAX_Y)):
            for x in range(self.BLOCK_MAX_X):
                if self.board[y][x].color is None:
                    upper = self.getUpperBlock(x, y)
                    if upper:
                        ux, uy = self.getBlockPos(upper)
                        self.board[uy][ux] = self.createBlockWithoutColor(
                            ux, uy)
                        self.board[y][x] = upper
                        ox, oy = self.getBlockOriginPos(x, y)
                        upper.moveTo(ox, oy)

    def getUpperBlock(self, x, y):
        for y in reversed(range(y)):
            if self.board[y][x].color:
                return self.board[y][x]
        return None

    def getBlockPos(self, block):
        for y, line in enumerate(self.board):
            for x, b in enumerate(line):
                if block == b:
                    return x, y
        # FIXME

    def boardColors(self):
        colors = []
        for line in self.board:
            l = []
            for b in line:
                l.append(b.color)
            colors.append(l)
        return colors

    def evaluateBoard(self):
        self.initEraseBlocks()
        self.evaluateBoardDirectionalX()
        self.evaluateBoardDirectionalY()
        self.chains = self.getChains()

    def evaluateBoardDirectionalX(self):
        for y in range(self.BLOCK_MAX_Y):
            for x in range(self.BLOCK_MAX_X - 2):
                b = self.board
                if b[y][x].color == b[y][x+1].color == b[y][x+2].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y][x+1] = b[y][x].color
                    self.eraseBlocks[y][x+2] = b[y][x].color

    def evaluateBoardDirectionalY(self):
        for y in range(self.BLOCK_MAX_Y - 2):
            for x in range(self.BLOCK_MAX_X):
                b = self.board
                if b[y][x].color == b[y+1][x].color == b[y+2][x].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y+1][x] = b[y][x].color
                    self.eraseBlocks[y+2][x] = b[y][x].color

    def getChains(self):
        chains = []
        for y in range(self.BLOCK_MAX_Y):
            for x in range(self.BLOCK_MAX_X):
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
        if x < self.BLOCK_MAX_X - 1:
            self.getChain(x+1, y, color, posList)
        if y > 0:
            self.getChain(x, y-1, color, posList)
        if y < self.BLOCK_MAX_Y - 1:
            self.getChain(x, y+1, color, posList)

        posList.append(Pos(x, y))
        return posList

    def getBlockOriginPos(self, x, y):
        size = self.blockSize
        return x * size + size / 2, y * size + size / 2

    def draw(self):
        pyxel.cls(0)

        if pyxel.btn(pyxel.KEY_SPACE):
            r = self.blockSize / 2
            for y, line in enumerate(self.board):
                for x, b in enumerate(line):
                    # b.draw()
                    ox, oy = self.getBlockOriginPos(x, y)
                    pyxel.circ(ox, oy, r, b.color)
            return

        for line in self.board:
            for b in line:
                if self.hasBlock != b:
                    b.draw()

        if self.hasBlock:
            self.hasBlock.draw()


App()
