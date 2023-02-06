class Row:
    def __init__(self, t):
        self.cells = t
        self.x = None
        self.y = None
    def __repr__(self):
        return str(self.__dict__)

