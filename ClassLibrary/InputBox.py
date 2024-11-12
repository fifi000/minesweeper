import pygame
from colors import *
from Global import *
from .Button import Button


class InputBox:
    def __init__(
        self,
        win,
        box_x,
        box_y,
        input_rows,
        texts,
        font,
        max_input,
        gap,
        middle_gap,
        scale_h=2.0,
        scale_w=1.1,
    ):
        self.win = win

        self.box_x = box_x
        self.box_y = box_y

        self.input_rows = input_rows
        self.rows = input_rows + 1
        self.rows_y = []
        self.texts = texts
        self.font = font
        self.roundness = 30

        self.max_text = self.font.render(find_longest(self.texts), True, WHITE)
        self.max_input = self.font.render(max_input, True, WHITE)

        self.gap = gap
        self.middle_gap = middle_gap
        self.scale_h = scale_h
        self.scale_w = scale_w

        self.width = (
            2 * self.gap
            + self.max_text.get_width()
            + middle_gap
            + self.scale_w * self.max_input.get_width()
        )
        self.height = self.scale_h * self.max_text.get_height() * self.rows

        self.add_rows_y()

        # submit button
        name = 'SUBMIT'
        text = self.font.render(name, True, BLACK)
        width = text.get_width() * self.scale_w
        height = text.get_height()
        x = self.box_x + self.width - self.gap - width
        y = self.box_y + self.height - (self.height / self.rows + height) / 2
        self.submit = Button(x, y, width, height, text)

        # input boxes
        self.input_boxes = []
        self.add_input_boxes()

    def add_input_boxes(self):
        x = self.box_x + self.width - (self.gap + self.max_input.get_width())

        for i in range(self.input_rows):
            y = self.rows_y[i]
            w, h = self.max_input.get_width(), self.max_input.get_height()
            box = Button(x, y, w, h)
            self.input_boxes.append(box)

    def add_rows_y(self):
        y = (
            self.box_y
            + (self.height / (self.input_rows + 1) - self.max_text.get_height()) / 2
        )

        for _ in range(self.input_rows):
            self.rows_y.append(y)
            y += self.height / self.rows

    def draw(self):
        self.draw_main_box()
        self.draw_texts()
        self.draw_input_boxes()
        self.draw_submit()

    def draw_main_box(self):
        pygame.draw.rect(
            self.win,
            BLACK,
            (self.box_x, self.box_y, self.width, self.height),
            0,
            self.roundness,
        )

    def draw_texts(self):
        x = self.box_x + self.gap

        for i, text in enumerate(self.texts):
            text = self.font.render(text.upper(), True, WHITE)
            self.win.blit(text, (x, self.rows_y[i]))

    def draw_submit(self):
        x, y = self.submit.pos
        pygame.draw.rect(
            self.win,
            WHITE,
            (self.submit.pos, (self.submit.width, self.submit.height)),
            0,
            self.roundness,
        )
        x += (self.submit.width - self.submit.text.get_width()) / 2
        self.win.blit(self.submit.text, (x, y))

    def draw_input_boxes(self):
        width = 3

        for button in self.input_boxes:
            text = self.font.render(button.name, True, BLACK)
            if button.clicked:
                x, y = button.x - width, button.y - width
                w, h = button.width + 2 * width, button.height + 2 * width
                pygame.draw.rect(self.win, GRAY, (x, y, w, h), width)
            pygame.draw.rect(
                self.win, WHITE, (button.x, button.y, button.width, button.height)
            )
            x = button.x + (button.width - text.get_width()) / 2
            y = button.y + (button.height - text.get_height()) / 2
            self.win.blit(text, (x, y))

    def collision(self, x, y):
        return (
            self.box_x <= x <= self.box_x + self.width
            and self.box_y <= y <= self.box_y + self.height
        )
