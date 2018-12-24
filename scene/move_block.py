import pyxel
from .base import GameSceneBase


class MoveBlockScene(GameSceneBase):

    def __init__(self, root, board):
        super(MoveBlockScene, self).__init__(root, board)
        self.blockSize = int(pyxel.width / board.width)
        self.draggingBlock = None

    def dragging(self):
        return self.draggingBlock is not None

    def update(self):
        super(MoveBlockScene, self).update()
        # ブロック持つ判定
        for line in self.board:
            for b in line:
                if not self.dragging() and pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                    if b.isHit(pyxel.mouse_x, pyxel.mouse_y):
                        self.draggingBlock = b

        # ブロックを離す判定
        if self.dragging() and not pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
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
                            # 見た目上の位置を入れ替える（アニメーション）
                            tx = b.targetX
                            ty = b.targetY
                            b.moveTo(self.draggingBlock.targetX,
                                     self.draggingBlock.targetY)
                            self.draggingBlock.targetX = tx
                            self.draggingBlock.targetY = ty
                            # board上の位置を入れ替える。
                            x1, y1 = self.board.getBlockPos(self.draggingBlock)
                            x2, y2 = self.board.getBlockPos(b)
                            self.board[y1][x1] = b
                            self.board[y2][x2] = self.draggingBlock

    def draw(self):
        super(MoveBlockScene, self).draw()
        for line in self.board:
            for b in line:
                if self.draggingBlock != b:
                    b.draw()

        if self.dragging():
            self.draggingBlock.draw()
