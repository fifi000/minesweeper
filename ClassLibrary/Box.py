import pygame
from colors import *
from .Button import Button


class Box:
    gap = 10

    def __init__(
        self,
        win,
        text,
        font,
        win_width,
        win_height,
        play_obj,
        repeat_obj,
        best_time,
        best_time_font,
    ):
        self.win = win
        self.width, self.height = win_width, win_height
        self.main_msg = font.render(text, True, WHITE)
        self.best_time_msg = best_time_font.render(f'Best: {best_time}s', True, WHITE)
        self.play = play_obj
        self.repeat = repeat_obj
        self.best_time = best_time

        self.roundness = 30

        # box
        self.box_w = 2 * Box.gap + self.main_msg.get_width()
        self.box_h = (
            4 * Box.gap
            + 3 * self.main_msg.get_height()
            + self.best_time_msg.get_height()
        )
        self.box_x, self.box_y = (
            (self.width - self.box_w) / 2,
            (self.height - self.box_h) / 2,
        )

        # play button
        x = self.box_x + (self.box_w - self.play.get_width()) / 2
        y = self.box_y + self.box_h - Box.gap - self.play.get_height()
        self.play_button = Button(x, y, self.play.get_width(), self.play.get_height())

        # repeat button
        x = self.box_x + self.box_w - self.repeat.get_width() - 2 * Box.gap
        y = self.box_y + self.box_h - self.repeat.get_height() - 2 * Box.gap
        self.repeat_button = Button(
            x, y, self.repeat.get_width(), self.repeat.get_height()
        )

    def draw(self):
        # background
        pygame.draw.rect(
            self.win,
            BLACK,
            (self.box_x, self.box_y, self.box_w, self.box_h),
            0,
            self.roundness,
        )

        # display text
        x = self.box_x + (self.box_w - self.main_msg.get_width()) / 2
        y = self.box_y + Box.gap
        self.win.blit(self.main_msg, (x, y))

        # best time text
        x = self.box_x + (self.box_w - self.best_time_msg.get_width()) / 2
        y += self.main_msg.get_height() + Box.gap
        self.win.blit(self.best_time_msg, (x, y))

        # play
        self.win.blit(self.play, (self.play_button.x, self.play_button.y))

        # repeat
        self.win.blit(self.repeat, (self.repeat_button.x, self.repeat_button.y))
