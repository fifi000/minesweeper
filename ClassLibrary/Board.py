import pygame
from Saper.colors import *
from Saper.Global import *
from .Button import Button


class Board:

    def __init__(self, win, rows, cols, width, height, scale, sq_size, line, roundness, level_name):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

        self.scale = scale
        self.sq_size = sq_size
        self.line = line
        self.roundness = roundness

        self.best_time = None

        # font
        font1_size = round(20 * self.scale)
        self.level_font = pygame.font.SysFont('consolas', font1_size, True)
        font2_size = round(30 * self.scale)
        self.upper_font = pygame.font.SysFont('consolas', font2_size, True)

        # upper part with head and clock | size with shadows
        self.upper_width = width
        self.upper_height = 2 * self.sq_size

        # importing flag and timer
        self.flag = self.import_photo(photos["flag"])
        self.timer = self.import_photo(photos["timer"])
        self.time = 0
        self.flags = 5

        # level
        self.level = level_name
        self.levels_names = ["EASY", "MEDIUM", "HARD", "CUSTOM"]
        self.levels = []

        text = self.level_font.render(self.level, True, WHITE)
        scale_w, scale_h = 1.6, 2
        if self.level == self.levels_names[-1]:
            scale_w = 1.3

        w, h = text.get_width() * scale_w, text.get_height() * scale_h
        x, y = (self.upper_width / 3 - w) / 2, (self.upper_height - h) / 2

        self.level_button = Button(x, y, w, h, text, self.level, WHITE, scale_w, scale_h)

        self.add_level_buttons()

        self.bg_levels_rect = self.add_bg_levels()

    def import_photo(self, source, k=1.0):
        img = pygame.image.load(source)
        scale = self.sq_size / img.get_height() * k
        w, h = round(img.get_height() * scale), round(img.get_width() * scale)

        return pygame.transform.scale(img.convert_alpha(), (w, h))

    def add_bg_levels(self):
        longest = find_longest(self.levels_names)
        longest = self.level_font.render(longest, True, WHITE)

        width = longest.get_width() * self.level_button.scale_w
        height = self.level_button.height
        x, y = self.level_button.pos

        y += height * 1.1
        height *= len(self.levels)

        return x, y, width, height

    def add_level_buttons(self):
        longest = find_longest(self.levels_names)
        longest = self.level_font.render(longest, True, WHITE)
        width = longest.get_width() * self.level_button.scale_w
        height = self.level_button.height
        x, y = self.level_button.pos
        y += height * 1.1
        for i in range(len(self.levels_names)):
            name = self.levels_names[i]
            color = WHITE
            if self.level == name:
                color = GRAY
            text = self.level_font.render(name, True, color)
            button = Button(x, y, width, height, text, name, color)
            self.levels.append(button)
            y += height

    def display_upper(self, temp, photo, part):
        text = self.upper_font.render(temp, True, WHITE)
        test_text = self.upper_font.render("000", True, WHITE)

        x = part * self.upper_width + (1 / 3 * self.upper_width - (photo.get_width() + test_text.get_width())) / 2
        y = (self.upper_height - photo.get_height()) / 2
        self.win.blit(photo, (x, y))

        x += photo.get_width() * 1.2
        y = (self.upper_height - test_text.get_height()) / 2
        self.win.blit(text, (x, y))

    def draw(self):
        self.win.fill(GRAY)

        # vertical grid lines
        count = self.cols - 1
        start_x, start_y = self.sq_size + self.line / 2, self.upper_height
        end_x, end_y = start_x, self.height

        for _ in range(count):
            pygame.draw.line(self.win, DARK_GREY, (start_x, start_y), (end_x, end_y), self.line)
            start_x += self.line + self.sq_size
            end_x = start_x

        # horizontal grid lines
        count = self.rows - 1
        start_x, start_y = 0, self.upper_height + self.sq_size + self.line / 2
        end_x, end_y = self.width, start_y

        for _ in range(count):
            pygame.draw.line(self.win, DARK_GREY, (start_x, start_y), (end_x, end_y), self.line)
            start_y += self.line + self.sq_size
            end_y = start_y

        self.draw_upper()

        # test
        # pygame.draw.line(self.win, BLACK, (self.width / 2, 0), (self.width / 2, self.height))
        # pygame.draw.line(self.win, BLACK, (self.width * 1/3, 0), (self.width * 1/3, self.height))
        # pygame.draw.line(self.win, BLACK, (self.width * 2/3, 0), (self.width * 2/3, self.height))

    def draw_upper(self):
        pygame.draw.rect(self.win, DARK_GREY, (0, 0, self.upper_width, self.upper_height))

        # level
        x, y = self.level_button.pos
        w, h = self.level_button.width, self.level_button.height
        pygame.draw.rect(self.win, BLACK, (x, y, w, h), 0, self.roundness)
        text = self.level_button.text
        x, y = (self.upper_width / 3 - text.get_width()) / 2, (self.upper_height - text.get_height()) / 2
        self.win.blit(text, (x, y))

        # flags
        flags = str(self.flags)
        while len(flags) < 3 and flags[0] != "-":
            flags = "0" + flags
        self.display_upper(flags, self.flag, 1 / 3)

        # time
        time = str(self.time)
        while len(time) < 3 and len(time) != 4:
            time = "0" + time
        self.display_upper(time, self.timer, 2 / 3)

    def draw_levels(self):

        pygame.draw.rect(self.win, BLACK, self.bg_levels_rect, 0, self.roundness)

        for button in self.levels:
            x, y = button.pos
            self.draw_text(x, y, button.width, button.height, button.name, button.color)

    def draw_text(self, x, y, width, height, text, color):
        text = self.level_font.render(text, True, color)
        x += (width - text.get_width()) / 2
        y += (height - text.get_height()) / 2
        self.win.blit(text, (x, y))
