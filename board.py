from block import Block


class Board:

    def __init__(self, width, height):
        self.board = []
        self.width = width
        self.height = height
        self.init()

    def init(self):
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(Block.create(x, y))
            self.board.append(line)

    def getBlockPos(self, block):
        for y, line in enumerate(self.board):
            for x, b in enumerate(line):
                if block == b:
                    return x, y

    def doneAnimation(self):
        for line in self.board:
            for b in line:
                if b.animation:
                    return False
        return True

    def __iter__(self):
        return self.board.__iter__()

    def __getitem__(self, i):
        return self.board[i]
