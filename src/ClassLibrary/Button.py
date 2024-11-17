class Button:

    def __init__(self, x, y, width, height, text=None, name="", color=None, scale_w=1.0, scale_h=1.0):
        self.x = x
        self.y = y
        self.pos = self.x, self.y
        self.width = width
        self.height = height

        self.name = name
        self.text = text

        self.color = color

        self.scale_w = scale_w
        self.scale_h = scale_h
        self.clicked = False

        self.temp = False

    def collision(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
