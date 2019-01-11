from .base import GameSceneBase


class WaitAnimation(GameSceneBase):
    def __init__(self, nextScene, sleep=0):
        super(WaitAnimation, self).__init__(nextScene.root, nextScene.board)
        self.nextScene = nextScene
        self.sleep = sleep

    def update(self):
        super(WaitAnimation, self).update()
        if self.board.doneAnimation():
            if self.sleep <= 0:
                self.root.changeScene(self.nextScene)
            self.sleep -= 1

    def draw(self):
        super(WaitAnimation, self).draw()
        self.drawBoard()
