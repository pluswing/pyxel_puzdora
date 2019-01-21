import pyxel
from .base import GameSceneBase


class MoveBlockScene(GameSceneBase):

    def __init__(self, root, board):
        super().__init__(root, board)
        self.blockSize = int(pyxel.width / board.width)
        self.draggingBlock = None
        self.finish = False

    def dragging(self):
        return self.draggingBlock is not None

    def update(self):
        super().update()
        # ブロック持つ判定
        for line in self.board:
            for b in line:
                if not self.dragging() and pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                    if b.isHit(pyxel.mouse_x, pyxel.mouse_y):
                        self.draggingBlock = b

        # ブロックを離す判定
        if self.dragging() and not pyxel.btn(pyxel.MOUSE_LEFT_BUTTON) or self.finish:
            self.draggingBlock.moveTo(
                self.draggingBlock.targetX, self.draggingBlock.targetY)
            self.draggingBlock = None
            self.root.nextScene(self)

        # ブロックの移動
        if self.dragging():
            self.draggingBlock.x = pyxel.mouse_x
            self.draggingBlock.y = pyxel.mouse_y

            # ブロックの入れ替え
            for line in self.board:
                for b in line:
                    if b.isHit(pyxel.mouse_x, pyxel.mouse_y) and not b.animation:
                        if self.draggingBlock != b:
                            dx, dy = self.board.getBlockPos(self.draggingBlock)
                            bx, by = self.board.getBlockPos(b)
                            if dx != bx and dy != by:
                                lr = self.board[dy][dx + (bx - dx)]
                                self.swap(self.draggingBlock, lr)
                            self.swap(self.draggingBlock, b)
                            pyxel.play(0, [20])

    def swap(self, b1, b2):
        # 見た目上の位置を入れ替える（アニメーション）
        tx = b2.targetX
        ty = b2.targetY
        b2.moveTo(b1.targetX,
                  b1.targetY)
        b1.targetX = tx
        b1.targetY = ty

        # board上の位置を入れ替える。
        x1, y1 = self.board.getBlockPos(b1)
        x2, y2 = self.board.getBlockPos(b2)
        self.board[y1][x1] = b2
        self.board[y2][x2] = b1

    def draw(self):
        super().draw()
        for line in self.board:
            for b in line:
                if self.draggingBlock != b:
                    b.draw()

        if self.dragging():
            self.draggingBlock.draw()
