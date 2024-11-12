class Square:
    def __init__(self, x, y, row, col):
        self.x = x
        self.y = y

        self.row = row
        self.col = col

        self.mine = False
        self.number = -1  # mine -1, empty 0, rest 1-8
        self.clicked = False
        self.checked = False
        self.flagged = False
        self.mine_clicked = False
