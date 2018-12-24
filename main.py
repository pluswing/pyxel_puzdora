import pyxel
import math
from block import Block
from pos import Pos
from board import Board

SCREEN_WIDTH = 250
BLOCK_MAX_Y = 5
BLOCK_MAX_X = 6


class GameSceneBase:
    def __init__(self, root, board):
        self.root = root
        self.board = board  # Board(BLOCK_MAX_X, BLOCK_MAX_Y)

    def name(self):
        return self.__class__.__name__

    def update(self):
        # ブロックのアップデートは必ずやる
        for line in self.board:
            for b in line:
                b.update()

    def draw(self):
        pyxel.cls(0)

    def drawBoard(self):
        for line in self.board:
            for b in line:
                b.draw()


class MoveBlockScene(GameSceneBase):

    def __init__(self, root, board):
        super(MoveBlockScene, self).__init__(root, board)
        self.blockSize = int(SCREEN_WIDTH / BLOCK_MAX_X)
        self.hasBlock = None

    def update(self):
        super(MoveBlockScene, self).update()
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
            self.root.changeScene(Evaluate(self.root, self.board))

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
                            x1, y1 = self.board.getBlockPos(self.hasBlock)
                            x2, y2 = self.board.getBlockPos(b)
                            self.board[y1][x1] = b
                            self.board[y2][x2] = self.hasBlock

    def draw(self):
        super(MoveBlockScene, self).draw()
        for line in self.board:
            for b in line:
                if self.hasBlock != b:
                    b.draw()

        if self.hasBlock:
            self.hasBlock.draw()


class Evaluate(GameSceneBase):

    def __init__(self, root, board):
        super(Evaluate, self).__init__(root, board)
        self.colors = []
        self.eraseBlocks = []

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
        for y in range(BLOCK_MAX_Y):
            self.eraseBlocks.append([0 for x in range(BLOCK_MAX_X)])

    def evaluateBoard(self):
        self.initEraseBlocks()
        self.evaluateBoardDirectionalX()
        self.evaluateBoardDirectionalY()
        return self.getChains()

    def evaluateBoardDirectionalX(self):
        for y in range(BLOCK_MAX_Y):
            for x in range(BLOCK_MAX_X - 2):
                b = self.board
                if b[y][x].color == b[y][x+1].color == b[y][x+2].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y][x+1] = b[y][x].color
                    self.eraseBlocks[y][x+2] = b[y][x].color

    def evaluateBoardDirectionalY(self):
        for y in range(BLOCK_MAX_Y - 2):
            for x in range(BLOCK_MAX_X):
                b = self.board
                if b[y][x].color == b[y+1][x].color == b[y+2][x].color:
                    self.eraseBlocks[y][x] = b[y][x].color
                    self.eraseBlocks[y+1][x] = b[y][x].color
                    self.eraseBlocks[y+2][x] = b[y][x].color

    def getChains(self):
        chains = []
        for y in range(BLOCK_MAX_Y):
            for x in range(BLOCK_MAX_X):
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
        if x < BLOCK_MAX_X - 1:
            self.getChain(x+1, y, color, posList)
        if y > 0:
            self.getChain(x, y-1, color, posList)
        if y < BLOCK_MAX_Y - 1:
            self.getChain(x, y+1, color, posList)

        posList.append(Pos(x, y))
        return posList

    def update(self):
        super(Evaluate, self).update()
        chains = self.evaluateBoard()
        if len(chains):
            self.root.changeScene(ChainBlocks(self.root, self.board, chains))
        else:
            self.root.changeScene(MoveBlockScene(self.root, self.board))

    def draw(self):
        super(Evaluate, self).draw()
        self.drawBoard()


class ChainBlocks(GameSceneBase):
    def __init__(self, root, board, chains):
        super(ChainBlocks, self).__init__(root, board)
        self.chains = chains

    def update(self):
        super(ChainBlocks, self).update()
        for chain in self.chains:
            for pos in chain:
                self.board[pos.y][pos.x].color = None

        self.root.changeScene(DropDown(self.root, self.board))

    def draw(self):
        super(ChainBlocks, self).draw()
        self.drawBoard()


class DropDown(GameSceneBase):
    def __init__(self, root, block):
        super(DropDown, self).__init__(root, block)

    def dropDownBlocks(self):
        for y in reversed(range(BLOCK_MAX_Y)):
            for x in range(BLOCK_MAX_X):
                if self.board[y][x].color is None:
                    upper = self.getUpperBlock(x, y)
                    if upper:
                        ux, uy = self.board.getBlockPos(upper)
                        self.board[uy][ux] = Block.createBlockWithoutColor(
                            ux, uy)
                        self.board[y][x] = upper
                        ox, oy = Block.calcBlockPos(x, y)
                        upper.moveTo(ox, oy)

    def getUpperBlock(self, x, y):
        for y in reversed(range(y)):
            if self.board[y][x].color:
                return self.board[y][x]
        return None

        # FIXME

    def update(self):
        super(DropDown, self).update()
        self.dropDownBlocks()
        self.root.changeScene(WaitAnimation(Fill(self.root, self.board)))

    def draw(self):
        super(DropDown, self).draw()
        self.drawBoard()


class WaitAnimation(GameSceneBase):
    def __init__(self, nextScene):
        super(WaitAnimation, self).__init__(nextScene.root, nextScene.board)
        self.nextScene = nextScene

    def update(self):
        super(WaitAnimation, self).update()
        if self.board.doneAnimation():
            self.root.changeScene(self.nextScene)

    def draw(self):
        super(WaitAnimation, self).draw()
        self.drawBoard()


class Fill(GameSceneBase):
    def __init__(self, root, block):
        super(Fill, self).__init__(root, block)

    def fillBlocks(self):
        maxDown = self.findMaxDown()
        self.fill(maxDown)

    def findMaxDown(self):
        maxDown = 0
        for x in range(BLOCK_MAX_X):
            down = 0
            for y in range(BLOCK_MAX_Y):
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
        super(Fill, self).update()
        self.fillBlocks()
        self.root.changeScene(WaitAnimation(Evaluate(self.root, self.board)))

    def draw(self):
        super(Fill, self).draw()
        self.drawBoard()


class App:
    def __init__(self):
        # new Board
        Block.BLOCK_SIZE = int(SCREEN_WIDTH / BLOCK_MAX_X)
        board = Board(BLOCK_MAX_X, BLOCK_MAX_Y)
        self.scene = MoveBlockScene(self, board)
        pyxel.init(SCREEN_WIDTH, math.floor(
            int(SCREEN_WIDTH / BLOCK_MAX_X) * BLOCK_MAX_Y))
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        print(self.scene.name())
        self.scene.update()

    def draw(self):
        self.scene.draw()

    def changeScene(self, newScene):
        self.scene = newScene


App()
