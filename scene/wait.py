from .base import GameSceneBase


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
