from block import Block


class Board:

    def __init__(self, width, height):
        self.board = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(Block.createBlock(x, y))
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
