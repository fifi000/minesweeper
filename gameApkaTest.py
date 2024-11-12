import pygame
import random
import time
import os.path
from colors import *
from Global import *
from ClassLibrary.Board import Board
from ClassLibrary.Box import Box
from ClassLibrary.Square import Square
from ClassLibrary.InputBox import InputBox


pygame.init()
pygame.display.set_caption("Saper")


class Game:

    playing_again = False
    first = [0, 0]

    def __init__(self, level_name, rows=10, cols=10, mines=0.15625):

        self.level_name = level_name
        self.line_thickness = 2

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
        number_font_size = round(30 * self.scale)
        self.number_font = pygame.font.SysFont('consolas', number_font_size, False)
        best_time_font_size = round(20 * self.scale)
        self.best_time_font = pygame.font.SysFont('consolas', best_time_font_size, False)

        # bools
        self.end = False
        self.draw_end_once = False
        self.playing = True
        self.custom = False
        self.if_win = False
        self.if_lose = False
        self.new_game = False
        self.if_score_saved = False

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
        self.best_time = self.get_best_score(self.level_name)

        # window
        self.width = self.sq_size * self.cols + (self.cols - 1) * self.line_thickness
        self.height = self.sq_size * self.rows + (self.rows - 1) * self.line_thickness + 2 * self.sq_size
        self.win = pygame.display.set_mode((self.width, self.height))

        # board
        self.board = Board(self.win, self.rows, self.cols, self.width, self.height, self.scale, self.sq_size,
                           self.line_thickness, self.roundness, self.level_name)

        self.board.flags = self.mines
        self.board.sq_size = self.sq_size
        self.board.scale = self.scale
        self.board.line = self.line_thickness
        self.board.roundness = self.roundness
        self.board.best_time = self.best_time

        # colors of numbers
        self.nums_colors = [BLUE, GREEN, RED, DARK_BLUE, DARK_RED, YELLOW, BLACK, ORANGE]

        # list of square objects
        self.squares = []
        self.add_squares()
        if Game.playing_again:
            self.load_previous_board()

        # importing photos
        self.timer = self.import_photo(photos["timer"], 0.7)
        self.bomb = self.import_photo(photos["bomb"], 0.7)
        self.flag = self.import_photo(photos["flag"], 0.8)
        self.X = self.import_photo(photos["X"], 0.6)
        self.x_test = self.import_photo(photos["x_test"], 0.6)
        self.play = self.import_photo(photos["play"], 1.8)
        self.repeat = self.import_photo(photos["repeat"], 0.6)

        self.custom_input = self.custom_init_fun()

        # winning box
        self.winning_box = Box(self.win, "You won!", self.number_font, self.width, self.height,
                               self.play, self.repeat, self.best_time, self.best_time_font)

        self.losing_box = Box(self.win, "You lost!", self.number_font, self.width, self.height,
                              self.play, self.repeat, self.best_time, self.best_time_font)

    def import_photo(self, source, k=1.0):
        img = pygame.image.load(source)
        scale = self.sq_size / img.get_height() * k
        w, h = round(img.get_height() * scale), round(img.get_width() * scale)
        return pygame.transform.scale(img.convert_alpha(), (w, h))

    def set_level_settings(self):
        if self.level_name == "MEDIUM":
            self.rows = 14
            self.cols = 18
            self.scale = 1.6
            self.mines_percent = 0.15873
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
                        if row + i < 0 or row + i >= self.rows or col + j < 0 or col + j >= self.cols or (
                                i == 0 and j == 0):
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

                if Game.playing_again and square.row == Game.first[0] and square.col == Game.first[1]:
                    self.draw_object(None, square, True, GREEN)

                if square.clicked and not square.mine:

                    pygame.draw.rect(self.win, LIGHT_GREY,
                                     (square.x + self.line_thickness / 2, square.y + self.line_thickness / 2,
                                      self.sq_size, self.sq_size))

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
            self.losing_box.draw()
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
            pygame.draw.rect(self.win, square_color,
                             (square.x + self.line_thickness / 2, square.y + self.line_thickness / 2,
                              self.sq_size, self.sq_size))

        if img is not None:
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
                    pygame.draw.rect(self.win, LIGHT_GREY,
                                     (square.x + self.line_thickness / 2, square.y + self.line_thickness / 2,
                                      self.sq_size, self.sq_size))

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

    def save_current_board(self, first_row, first_col):
        path = "currentBoard.txt"

        file = open(path, "w")
        lines = []

        for row in self.squares:
            for square in row:
                first = 0

                if (first_row, first_col) == (square.row, square.col):
                    first = 1

                text = f"{square.row},{square.col},{square.number},{first}" + "\n"
                lines.append(text)

        file.writelines(lines)
        file.close()

    def load_previous_board(self):
        path = "currentBoard.txt"

        file = open(path, "r")
        lines = file.readlines()

        for line in lines:
            cols = line.split(",")

            row = int(cols[0])
            col = int(cols[1])
            number = int(cols[2])
            first = int(cols[3])

            self.squares[row][col].row = row
            self.squares[row][col].col = col
            self.squares[row][col].number = number

            if number == -1:
                self.squares[row][col].mine = True

            if first == 1:
                Game.first = [row, col]

        file.close()

    @staticmethod
    def upload_scores(path):
        output = []

        with open(path, "r") as file:
            lines = file.readlines()

            if len(lines) > 0:
                for line in lines:
                    cols = line.split(",")

                    output.append(int(cols[1]))

        return output

    @staticmethod
    def save_scores_to_file(path, scores):

        with open(path, "w") as file:
            lines = []

            for i, score in enumerate(scores):
                line = f"{i + 1},{score}\n"
                lines.append(line)

            file.writelines(lines)

    @staticmethod
    def save_best_score(user_score, level_name):
        # place_number, score
        path = f"scores_{str(level_name).lower()}.txt"
        new_top_score = True

        scores = Game.upload_scores(path)

        # check if user score is greater than any score in scores
        if len(scores) == 10:
            new_top_score = False

            for score in scores:
                if user_score < score:
                    new_top_score = True
                    break

        if new_top_score:
            scores.append(user_score)

            # delete duplicates
            scores = set(scores)
            scores = list(scores)

            scores.sort()
            if len(scores) > 10:
                scores = scores[:10]

            Game.save_scores_to_file(path, scores)

    @staticmethod
    def get_best_score(level_name):
        path = f"scores_{level_name}.txt"

        if not os.path.exists(path):
            open(path, "w").close()

        file = open(path, "r+")

        score = 1000

        line = file.readline()

        if len(line) > 1:
            line = line.split(",")
            score = int(line[1])

        return score

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
                                    Game.playing_again = False
                                    return True, button.name

                        if not clicked:
                            self.board.level_button.clicked = False
                            self.draw_everything = True

                elif self.custom:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if self.custom_input.collision(mouse_x, mouse_y):

                            if self.custom_input.submit.collision(mouse_x, mouse_y):
                                Game.playing_again = False
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
                            Game.playing_again = False
                            return True, "CUSTOM"
                        for i, button in enumerate(self.custom_input.input_boxes):
                            if button.clicked:
                                if event.key == pygame.K_BACKSPACE:
                                    self.custom_input.input_boxes[i].name = button.name[:-1]
                                elif event.key == pygame.K_TAB:
                                    self.custom_input.input_boxes[i].clicked = False
                                    next_input_box = (i + 1) % len(self.custom_input.input_boxes)
                                    self.custom_input.input_boxes[next_input_box].clicked = True
                                elif event.unicode in [str(j) for j in range(10)] and len(button.name) < 2:
                                    self.custom_input.input_boxes[i].name += event.unicode

                                break

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.draw_everything = True
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if self.if_win:

                            if self.winning_box.play_button.collision(mouse_x, mouse_y):
                                self.new_game = True
                                return True, self.level_name

                            elif self.winning_box.repeat_button.collision(mouse_x, mouse_y):

                                Game.playing_again = True
                                self.new_game = True
                                return True, self.level_name

                        if self.if_lose:
                            if self.losing_box.play_button.collision(mouse_x, mouse_y):
                                self.new_game = True
                                return True, self.level_name

                            elif self.losing_box.repeat_button.collision(mouse_x, mouse_y):

                                Game.playing_again = True
                                self.new_game = True
                                return True, self.level_name

                        mouse_row, mouse_col = self.converter(mouse_x, mouse_y)

                        if not self.end and 0 <= mouse_row < self.rows and 0 <= mouse_col < self.cols:

                            square = self.squares[mouse_row][mouse_col]

                            if not square.clicked:

                                if self.click_counter == 0:

                                    if not Game.playing_again:
                                        square.number = 0
                                        self.foo(mouse_row, mouse_col)

                                        # save current board to file
                                        self.save_current_board(mouse_row, mouse_col)

                                    Game.playing_again = False
                                    self.start_time = time.time()

                                if event.button == 1 and \
                                        not (square.flagged or self.x_clicked or self.if_win or self.if_lose):
                                    square.clicked = True
                                    self.square_left -= 1
                                    self.click_counter += 1

                                    if square.number == 0:
                                        self.if_empty_square(mouse_row, mouse_col)

                                    elif square.mine:
                                        square.mine_clicked = True

                                elif event.button == 3 and not self.if_win and not self.if_lose:
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

            if self.end and self.square_left != self.mines:
                self.if_lose = True

            if self.if_win and not self.if_score_saved:
                self.save_best_score(round(time.time() - self.start_time), self.level_name)
                self.if_score_saved = True

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

            if game.new_game:
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

                    if mines > 1 / 3:
                        mines = 1 / 3

    pygame.quit()


main()
