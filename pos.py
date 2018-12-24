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
