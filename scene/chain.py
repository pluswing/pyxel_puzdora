import pyxel
from .base import GameSceneBase


class ChainScene(GameSceneBase):

    def __init__(self, root, board, chains, comboCounter):
        super().__init__(root, board)
        self.chains = chains
        self.comboCounter = comboCounter

    def update(self):
        super().update()
        if self.board.doneAnimation():
            if len(self.chains):
                chain = self.chains.pop(0)
                for pos in chain:
                    self.board[pos.y][pos.x].blink()
                pyxel.play(0, [self.comboCounter])
                self.comboCounter += 1
                # スコア計算 ブロック数 * ブロック数 * 100 * コンボ数
                score = len(chain) * len(chain) * 100 * self.comboCounter
                return score
            else:
                self.root.nextScene(self)
        return 0

    def draw(self):
        super().draw()
        self.drawBoard()
