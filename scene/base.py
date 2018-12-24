import pyxel


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
