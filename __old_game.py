import pygame, random, time
import os

pygame.font.init()

pygame.display.set_caption("Saper")

# colors
BLACK = (0, 0, 0)
LIGHT_BLACK = (20, 20, 20)

WHITE = (255, 255, 255)
LIGHT_GREY = (220, 220, 220)
GRAY = (160, 160, 160)
DARK_GREY = (120, 120, 120)

RED = (200, 0, 0)
DARK_RED = (150, 0, 0)

GREEN = (0, 170, 0)

BLUE = (45, 100, 245)
DARK_BLUE = (25, 80, 225)

YELLOW = (249, 215, 28)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)

photos = {}


def convert_photo(photo_name):
    real_path = os.path.realpath(__file__)
    index = real_path.rfind("\\")
    current_directory = real_path[:index]
    return os.path.join(current_directory, f"photos/{photo_name}")


def set_photos():
    names = ["bomb.png", "flag.png", "repeat.png", "timer.png", "X.png", "x_test.png"]
    for name in names:
        x = convert_photo(name)
        photos[name[:-4]] = x


def find_longest(A):
    longest = A[0]
    for el in A:
        if len(el) > len(longest):
            longest = el

    return longest


class Box:
    def __init__(self, win, text, font, win_width, win_height, repeat_obj):
        gap = 10
        self.win = win
        self.width, self.height = win_width, win_height
        self.text = text
        self.text = font.render(text, True, WHITE)
        self.repeat = repeat_obj

        self.roundness = 30

        self.box_w, self.box_h = 2 * gap + self.text.get_width(), 4 * self.text.get_height()
        self.box_x, self.box_y = (self.width - self.box_w) / 2, (self.height - self.box_h) / 2

        x = self.box_x + (self.box_w - self.repeat.get_width()) / 2
        y = self.box_y + 3/4 * self.box_h - self.repeat.get_height() / 2
        self.repeat_button = Button(x, y, self.repeat.get_width(), self.repeat.get_height())

    def draw(self):
        # background
        pygame.draw.rect(self.win, BLACK, (self.box_x, self.box_y, self.box_w, self.box_h), 0, self.roundness)

        # display text
        x = self.box_x + (self.box_w - self.text.get_width()) / 2
        y = self.box_y + self.box_h / 4 - self.text.get_height() / 2
        self.win.blit(self.text, (x, y))

        # repeat
        self.win.blit(self.repeat, (self.repeat_button.x, self.repeat_button.y))


class InputBox:
    def __init__(self, win, box_x, box_y, input_rows, texts, font, max_input, gap, middle_gap, scale_h=2.0, scale_w=1.1):
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

        self.width = 2 * self.gap + self.max_text.get_width() + middle_gap + self.scale_w * self.max_input.get_width()
        self.height = self.scale_h * self.max_text.get_height() * self.rows

        self.add_rows_y()

        # submit button
        name = "SUBMIT"
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
        y = self.box_y + (self.height / (self.input_rows + 1) - self.max_text.get_height()) / 2

        for _ in range(self.input_rows):
            self.rows_y.append(y)
            y += self.height / self.rows

    def draw(self):
        self.draw_main_box()
        self.draw_texts()
        self.draw_input_boxes()
        self.draw_submit()

    def draw_main_box(self):
        pygame.draw.rect(self.win, BLACK, (self.box_x, self.box_y, self.width, self.height), 0, self.roundness)

    def draw_texts(self):
        x = self.box_x + self.gap

        for i, text in enumerate(self.texts):
            text = self.font.render(text.upper(), True, WHITE)
            self.win.blit(text, (x, self.rows_y[i]))

    def draw_submit(self):
        x, y = self.submit.pos
        pygame.draw.rect(self.win, WHITE, (self.submit.pos, (self.submit.width, self.submit.height)), 0, self.roundness)
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
            pygame.draw.rect(self.win, WHITE, (button.x, button.y, button.width, button.height))
            x = button.x + (button.width - text.get_width()) / 2
            y = button.y + (button.height - text.get_height()) / 2
            self.win.blit(text, (x, y))

    def collision(self, x, y):
        return self.box_x <= x <= self.box_x + self.width and self.box_y <= y <= self.box_y + self.height


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

        x = part * self.upper_width + (1/3 * self.upper_width - (photo.get_width() + test_text.get_width())) / 2
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
        self.display_upper(flags, self.flag, 1/3)

        # time
        time = str(self.time)
        while len(time) < 3 and len(time) != 4:
            time = "0" + time
        self.display_upper(time, self.timer, 2/3)

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


class Game:
    def __init__(self, level_name, rows=10, cols=10, mines=0.15625):

        self.level_name = level_name
        self.line_thickness = 2

        # setting up photos
        set_photos()

        # rows, cols, scale, mines
        self.scale = 2
        self.rows, self.cols = rows, cols
        self.mines_percent = mines
        self.set_level_settings()
        self.mines = round(self.rows * self.cols * self.mines_percent)

        # consts
        self.roundness = 30
        self.sq_size = round(30 * self.scale)

        # fonts
        font_size = round(30 * self.scale)
        self.number_font = pygame.font.SysFont('Consolas', font_size, False)

        # bools
        self.end = False
        self.draw_end_once = False
        self.playing = True
        self.custom = False
        self.if_win = False
        self.repeated = False

        self.draw_everything = True

        # temp x to check
        self.x_clicked = False
        self.x_list = []

        # duperele
        self.square_left = self.rows * self.cols
        self.click_counter = 0
        self.not_mines = []

        # time
        self.start_time = 0
        self.playing_time = 0

        # window
        self.width = self.sq_size * self.cols + (self.cols - 1) * self.line_thickness
        self.height = self.sq_size * self.rows + (self.rows - 1) * self.line_thickness + 2 * self.sq_size
        self.win = pygame.display.set_mode((self.width, self.height))

        # board
        self.board = Board(self.win, self.rows, self.cols, self.width, self.height,self.scale, self.sq_size, self.line_thickness, self.roundness, self.level_name)

        self.board.flags = self.mines
        self.board.sq_size = self.sq_size
        self.board.scale = self.scale
        self.board.line = self.line_thickness
        self.board.roundness = self.roundness

        # colors of numbers
        self.nums_colors = [BLUE, GREEN, RED, DARK_BLUE, DARK_RED, YELLOW, BLACK, ORANGE]

        # list of square objects
        self.squares = []
        self.add_squares()

        # importing photos
        self.timer = self.import_photo(photos["timer"], 0.7)
        self.bomb = self.import_photo(photos["bomb"], 0.7)
        self.flag = self.import_photo(photos["flag"], 0.8)
        self.X = self.import_photo(photos["X"], 0.6)
        self.x_test = self.import_photo(photos["x_test"], 0.6)
        self.repeat = self.import_photo(photos["repeat"], 1.3)

        self.custom_input = self.custom_init_fun()

        # winning box

        self.winning_box = Box(self.win, "You won!", self.number_font, self.width, self.height, self.repeat)

    def import_photo(self, source, k=1.0):
        img = pygame.image.load(source)
        scale = self.sq_size / img.get_height() * k
        w, h = round(img.get_height() * scale), round(img.get_width() * scale)
        return pygame.transform.scale(img.convert_alpha(), (w, h))

    def set_level_settings(self):
        if self.level_name == "MEDIUM":
            self.rows = 16
            self.cols = 16
            self.scale = 1.4
            self.mines_percent = 0.15625
        elif self.level_name == "HARD":
            self.rows = 16
            self.cols = 30
            self.mines_percent = 0.209
            self.scale = 1.35
        elif self.level_name == "CUSTOM":
            if self.cols > 2 * self.rows:
                self.cols = 2 * self.rows
            if self.rows <= 10:
                self.scale = 2
            else:
                self.scale = 21.6 / self.rows
        else:
            self.rows = 10
            self.cols = 10
            self.mines_percent = 0.15625
            self.scale = 2

        if self.rows >= 15 or self.cols >= 15:
            self.line_thickness = 1

    def add_squares(self):

        for row in range(self.rows):
            temp_row = []
            for col in range(self.cols):
                x = col * (self.sq_size + self.line_thickness)
                y = self.board.upper_height + row * (self.sq_size + self.line_thickness)
                temp_row.append(Square(x, y, row, col))

            self.squares.append(temp_row)

    def add_mines(self):
        for _ in range(self.mines):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            while self.squares[row][col].mine or (row, col) in self.not_mines:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)

            self.squares[row][col].mine = True

    def add_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]

                if square.mine:
                    continue

                count = 0
                dirs = (-1, 0, 1)

                for i in dirs:
                    for j in dirs:
                        if row + i < 0 or row + i >= self.rows or col + j < 0 or col + j >= self.cols or (i == 0 and j == 0):
                            continue

                        if self.squares[row + i][col + j].mine:
                            count += 1

                square.number = count

    def if_empty_square(self, row, col):
        dirs = (-1, 0, 1)

        self.squares[row][col].checked = True

        for i in dirs:
            for j in dirs:
                x = row + i
                y = col + j

                if x < 0 or x >= self.rows or y < 0 or y >= self.cols or (i == 0 and j == 0):
                    continue

                if not self.squares[x][y].clicked:
                    self.squares[x][y].clicked = True
                    self.square_left -= 1

                    if self.squares[x][y].flagged:
                        self.board.flags += 1

                # self.draw()
                # pygame.time.delay(100)

                if self.squares[x][y].number == 0 and not self.squares[x][y].checked:
                    self.if_empty_square(x, y)

    def converter(self, x, y):

        row = (y - self.board.upper_height) // (self.sq_size + self.line_thickness)
        col = x // (self.sq_size + self.line_thickness)

        return row, col

    def foo(self, row, col):
        dirs = (-1, 0, 1)

        for i in dirs:
            for j in dirs:
                x = row + i
                y = col + j

                if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
                    continue

                self.not_mines.append((x, y))

        self.add_mines()
        self.add_numbers()

    def check_win(self):
        count = 0

        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]

                if not square.clicked:
                    count += 1

        return count == self.mines

    def draw(self):
        self.board.draw()

        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]

                if square.clicked and not square.mine:

                    pygame.draw.rect(self.win, LIGHT_GREY, (square.x + self.line_thickness/2, square.y + self.line_thickness/2, self.sq_size, self.sq_size))

                    if square.number > 0:
                        text = self.number_font.render(str(square.number), True, self.nums_colors[square.number - 1])
                        self.draw_object(text, square)

                elif square.flagged:
                    self.draw_object(self.flag, square)

                elif square.clicked and square.mine:
                    self.draw_object(self.bomb, square, True, RED)
                    self.end = True

        if self.end:
            self.draw_end()
            self.draw_end_once = True
        elif self.if_win:
            self.winning_box.draw()
        elif self.x_clicked:
            self.draw_test_x()

        if self.board.level_button.clicked:
            self.draw_levels()
            pygame.display.update()
        elif self.custom:
            self.custom_input.draw()
            pygame.display.update()
        else:
            pygame.display.update()

    def draw_levels(self):
        self.board.draw_levels()

    def draw_object(self, img, square, draw_square=False, square_color=LIGHT_GREY):
        if draw_square:
            pygame.draw.rect(self.win, square_color, (square.x + self.line_thickness / 2, square.y + self.line_thickness / 2, self.sq_size, self.sq_size))

        x = square.x + (self.sq_size - img.get_width()) / 2
        y = square.y + (self.sq_size - img.get_height()) / 2

        self.win.blit(img, (x, y))

    def draw_end(self):
        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]

                if square.mine and not square.clicked and not square.flagged:
                    self.draw_object(self.bomb, square, True)

                    if not self.draw_end_once:
                        pygame.display.update()
                        pygame.time.delay(20)
                
                elif square.flagged and not square.mine:
                    pygame.draw.rect(self.win, LIGHT_GREY, (square.x + self.line_thickness / 2, square.y + self.line_thickness / 2, self.sq_size, self.sq_size))

                    if square.number > 0:
                        text = self.number_font.render(str(square.number), True, self.nums_colors[square.number - 1])
                        self.draw_object(text, square)

                    # draw X
                    self.draw_object(self.X, square)

    def draw_test_x(self):
        for pos in self.x_list:
            row, col = pos
            square = self.squares[row][col]
            self.draw_object(self.x_test, square)

    def custom_init_fun(self):
        gap = 30
        x, y, width, height = self.board.bg_levels_rect

        texts = ["rows", "columns", "mines [%]"]

        return InputBox(self.win, x, y, 3, texts, self.board.level_font, "00,00", gap, 2 * gap)

    def main(self):

        while self.playing:

            if self.click_counter > 0 and not self.end and not self.if_win:
                self.playing_time = round(time.time() - self.start_time)
                self.board.time = self.playing_time

            if self.board.level_button.clicked or self.custom or self.end:
                self.draw_everything = True

            if self.draw_everything:
                self.draw()
            else:
                self.board.draw_upper()
                pygame.display.update()

            self.draw_everything = False

            for event in pygame.event.get():

                if self.board.level_button.clicked:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if event.type == pygame.MOUSEMOTION:

                        for i, button in enumerate(self.board.levels):
                            if button.collision(mouse_x, mouse_y):
                                # change all colors to white
                                for j in range(len(self.board.levels)):
                                    self.board.levels[j].color = WHITE

                                self.board.levels[i].color = GRAY
                                break

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = False
                        for button in self.board.levels:
                            if button.collision(mouse_x, mouse_y):
                                clicked = True
                                if button.name == "CUSTOM":
                                    self.custom = True
                                    self.custom_input.input_boxes[0].clicked = True
                                    self.board.level_button.clicked = False
                                else:
                                    return True, button.name

                        if not clicked:
                            self.board.level_button.clicked = False
                            self.draw_everything = True

                elif self.custom:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if self.custom_input.collision(mouse_x, mouse_y):

                            if self.custom_input.submit.collision(mouse_x, mouse_y):

                                return True, "CUSTOM"
                            for i, box in enumerate(self.custom_input.input_boxes):
                                if box.collision(mouse_x, mouse_y):

                                    for j in range(len(self.custom_input.input_boxes)):
                                        self.custom_input.input_boxes[j].clicked = False
                                    self.custom_input.input_boxes[i].clicked = True
                                    break
                        else:
                            self.custom = False
                            self.draw_everything = True

                            for i in range(len(self.custom_input.input_boxes)):
                                self.custom_input.input_boxes[i].clicked = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return True, "CUSTOM"
                        for i, button in enumerate(self.custom_input.input_boxes):
                            if button.clicked:
                                if event.key == pygame.K_BACKSPACE:
                                    self.custom_input.input_boxes[i].name = button.name[:-1]
                                elif event.key == pygame.K_TAB:
                                    self.custom_input.input_boxes[i].clicked = False
                                    next = (i + 1) % len(self.custom_input.input_boxes)
                                    self.custom_input.input_boxes[next].clicked = True
                                elif event.unicode in [str(j) for j in range(10)] and len(button.name) < 2:
                                    self.custom_input.input_boxes[i].name += event.unicode

                                break

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.draw_everything = True
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if self.if_win:
                            if self.winning_box.repeat_button.collision(mouse_x, mouse_y):
                                self.repeated = True
                                return True, self.level_name

                        mouse_row, mouse_col = self.converter(mouse_x, mouse_y)

                        if not self.end and 0 <= mouse_row < self.rows and 0 <= mouse_col < self.cols:

                            square = self.squares[mouse_row][mouse_col]

                            if not square.clicked:

                                if self.click_counter == 0:
                                    square.number = 0
                                    self.foo(mouse_row, mouse_col)
                                    self.start_time = time.time()

                                if event.button == 1 and not (square.flagged or self.x_clicked or self.if_win):
                                    square.clicked = True
                                    self.square_left -= 1
                                    self.click_counter += 1

                                    if square.number == 0:
                                        self.if_empty_square(mouse_row, mouse_col)

                                    elif square.mine:
                                        square.mine_clicked = True

                                elif event.button == 3 and not self.if_win:
                                    if square.flagged:
                                        square.flagged = False
                                        self.board.flags += 1
                                    elif self.x_clicked:
                                        pos = (mouse_row, mouse_col)
                                        if pos in self.x_list:
                                            self.x_list.remove(pos)
                                        else:
                                            self.x_list.append(pos)
                                    else:
                                        square.flagged = True
                                        self.board.flags -= 1

                        # check if level button is clicked
                        elif self.board.level_button.collision(mouse_x, mouse_y):
                            self.board.level_button.clicked = not self.board.level_button.clicked

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            if self.x_clicked:
                                self.x_list = []

                            self.x_clicked = not self.x_clicked
                            self.draw_everything = True

                if event.type == pygame.QUIT:
                    self.playing = False

            if not self.end and self.square_left == self.mines:
                self.if_win = True

        return False, None


def main():

    playing = True
    name = "EASY"
    rows, cols = 10, 10
    mines = 0.15625

    while playing:
        game = Game(name, rows, cols, mines)
        playing, name = game.main()

        if name == "CUSTOM":

            if game.repeated:
                rows = game.rows
                cols = game.cols
                mines = game.mines / 100
            else:
                rows = game.custom_input.input_boxes[0].name
                cols = game.custom_input.input_boxes[1].name
                mines = game.custom_input.input_boxes[2].name

                if rows == "" or cols == "":
                    rows = 10
                    cols = 10
                else:
                    rows = int(rows)
                    cols = int(cols)

                    if rows < 5:
                        rows = 5
                    if cols < 10:
                        cols = 10

                if mines == "":
                    mines = 0.15625
                else:
                    mines = float(mines) / 100

                    if mines > 1/3:
                        mines = 1/3

    pygame.quit()


main()
