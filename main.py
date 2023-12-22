from random_word import RandomWords
from tkinter import *
import pygame, sys, random, time

pygame.init()

pygame.display.set_caption('Word Search Solver')


#Icon = pygame.image.load('ws.png')


#pygame.display.set_icon(Icon)

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
BLUE = (0, 150, 255)
PURPLE = (75, 0, 130)

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

started = False

def random_letter():
    global letters
    return letters[random.randint(0, 25)]

def random_color():
    colors = [LIGHT_RED, ORANGE, DARK_GREEN, BLUE, PURPLE]
    return colors[random.randint(0, 4)]

class WordSearch:
    def __init__(self, num_words):
        global started
        started = True
        self.num_words = num_words
        self.BOARD_WIDTH = int(self.num_words * 1.25)
        self.BOARD_HEIGHT = self.BOARD_WIDTH

        if 10 <= self.num_words < 15:
            self.time_delay = 0.02
        elif 15 <= self.num_words <= 22:
            self.time_delay = 0.01
        else:
            self.time_delay = 0.003

        self.LETTER_FONT = pygame.font.Font('freesansbold.ttf', int((1 / self.BOARD_WIDTH) * 500))
        self.WORD_FONT = pygame.font.Font('freesansbold.ttf', int((1 / self.num_words) * 275))

        self.board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.board.append(temp)

        self.highlight_board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.highlight_board.append(temp)

        self.temp_highlight_board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.temp_highlight_board.append(temp)

        self.offset = 800 // self.BOARD_WIDTH

        self.rects = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append(pygame.Rect((j*self.offset + 200, i*self.offset), (self.offset, self.offset)))
            self.rects.append(temp)

        self.highlight = pygame.Surface((self.offset, self.offset))
        self.highlight.set_alpha(128)

        self.unchanging_word_list = []
        self.changing_word_list = []

        self.orgin_i = None
        self.orgin_j = None

    def reset(self):
        self.changing_word_list = []
        for i in range(len(self.unchanging_word_list)):
            self.changing_word_list.append(self.unchanging_word_list[i])

        self.highlight_board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.highlight_board.append(temp)

    def generate(self):
        self.unchanging_word_list = []

        self.reset()

        self.board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.board.append(temp)

        r = RandomWords()
        while len(self.unchanging_word_list) < self.num_words:
            word = r.get_random_word()
            if 3 < len(word) <= self.num_words - 1:
                self.unchanging_word_list.append(word.upper())

        self.unchanging_word_list.sort()
        self.changing_word_list = []
        for i in range(len(self.unchanging_word_list)):
            self.changing_word_list.append(self.unchanging_word_list[i])

        # print(self.board)
        active_list = self.unchanging_word_list
        # print(changing_word_list)
        while len(active_list) > 0:
            next_list = []
            for i in range(len(active_list)):
                num = random.randint(1, 2)
                if num == 1:
                    word = active_list[i][::-1]
                else:
                    word = active_list[i]

                word = active_list[i]
                num = random.randint(1, 4)
                count = 0
                if num == 1:
                    x, y = random.randint(0, self.BOARD_WIDTH - len(word)), random.randint(0, self.BOARD_HEIGHT - 1)
                    if self.board[y][x] == '':
                        for j in range(len(word)):
                            if self.board[y][x + j] == '' or self.board[y][x + j] == word[j]:
                                pass
                            else:
                                count += 1
                        if count > 0:
                            next_list.append(active_list[i])
                        else:
                            for j in range(len(word)):
                                self.board[y][x + j] = word[j]
                    else:
                        next_list.append(active_list[i])
                # verticals
                elif num == 2:
                    x, y = random.randint(0, self.BOARD_WIDTH - 1), random.randint(0, self.BOARD_HEIGHT - len(word))
                    if self.board[y][x] == '':
                        for j in range(len(word)):
                            if self.board[y + j][x] == '' or self.board[y + j][x] == word[j]:
                                pass
                            else:
                                count += 1
                        if count > 0:
                            next_list.append(active_list[i])
                        else:
                            for j in range(len(word)):
                                self.board[y + j][x] = word[j]
                    else:
                        next_list.append(active_list[i])
                # diagonal left
                elif num == 3:
                    x, y = random.randint(len(word) - 1, self.BOARD_WIDTH - 1), random.randint(0, self.BOARD_HEIGHT - len(word))
                    if self.board[y][x] == '':
                        for j in range(len(word)):
                            if self.board[y + j][x - j] == '' or self.board[y + j][x - j] == word[j]:
                                pass
                            else:
                                count += 1
                        if count > 0:
                            next_list.append(active_list[i])
                        else:
                            for j in range(len(word)):
                                self.board[y + j][x - j] = word[j]
                    else:
                        next_list.append(active_list[i])
                # diagonal right
                else:
                    x, y = random.randint(0, self.BOARD_WIDTH - len(word)), random.randint(0, self.BOARD_HEIGHT - len(word))
                    if self.board[y][x] == '':
                        for j in range(len(word)):
                            if self.board[y + j][x + j] == '' or self.board[y + j][x + j] == word[j]:
                                pass
                            else:
                                count += 1
                        if count > 0:
                            next_list.append(active_list[i])
                        else:
                            for j in range(len(word)):
                                self.board[y + j][x + j] = word[j]
                    else:
                        next_list.append(active_list[i])

            active_list = next_list

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.board[i][j] == '':
                    self.board[i][j] = random_letter()
        #print(self.board)

    def draw_board(self):

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                pygame.draw.rect(screen, GRAY, self.rects[i][j], 1)
                #pygame.draw.rect(screen, GRAY, (j*self.offset + 200, i*self.offset, self.offset, self.offset), 1)
                screen.blit(self.LETTER_FONT.render(self.board[i][j], True, BLACK), (j*self.offset + 200 + self.offset // 4, i*self.offset + self.offset // 4))

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.highlight_board[i][j] != '':
                    self.highlight.fill(self.highlight_board[i][j])
                    screen.blit(self.highlight, (j * self.offset + 200, i * self.offset))

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.temp_highlight_board[i][j] != '':
                    self.highlight.fill(GREEN)
                    screen.blit(self.highlight, (j * self.offset + 200, i * self.offset))

    def draw_word_list(self):
        pygame.draw.rect(screen, LIGHT_RED, (0, 0, 200, 800))
        for i in range(len(self.unchanging_word_list)):
            if self.unchanging_word_list[i] in self.changing_word_list:
                screen.blit(self.WORD_FONT.render(self.unchanging_word_list[i], True, BLACK), (5, (i * (SCREEN_HEIGHT - 240) // self.num_words + 5) + 240))
            else:
                screen.blit(self.WORD_FONT.render(self.unchanging_word_list[i], True, BLACK), (5, (i * (SCREEN_HEIGHT - 240) // self.num_words + 5) + 240))
                screen.blit(self.WORD_FONT.render("-" * len(self.unchanging_word_list[i] * 2), True, WHITE), (5, (i * (SCREEN_HEIGHT - 240) // self.num_words + 5) + 240))

    def clear_temp_highlights(self):
        self.temp_highlight_board = []
        for i in range(self.BOARD_HEIGHT):
            temp = []
            for j in range(self.BOARD_WIDTH):
                temp.append('')
            self.temp_highlight_board.append(temp)

    def check_player_highlights(self):
        word = []
        coords = []
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.temp_highlight_board[i][j] == GREEN:
                    word.append(self.board[i][j])
                    coords.append((i,j))
        word = ''.join(word)
        #self.clear_temp_highlights()
        if word in self.changing_word_list:
            color = random_color()
            for i in range(len(coords)):
                self.highlight_board[coords[i][0]][coords[i][1]] = color
            self.changing_word_list.remove(word)


    def player_input(self):
        global started
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(self.board)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for i in range(self.BOARD_HEIGHT):
                        for j in range(self.BOARD_WIDTH):
                            if self.rects[i][j].collidepoint(pygame.mouse.get_pos()):
                                self.orgin_i = i
                                self.orgin_j = j
                                self.temp_highlight_board[i][j] = GREEN
                                #print(1, self.orgin_i, self.orgin_j)

        if solve_button.draw():
            self.solve()
        if reset_button.draw():
            self.reset()
        if generate_button.draw():
            self.generate()
        if menu_button.draw():
            started = False

        if pygame.mouse.get_pressed()[0]:
            for i in range(self.BOARD_HEIGHT):
                for j in range(self.BOARD_WIDTH):
                    if self.rects[i][j].collidepoint(pygame.mouse.get_pos()):
                        self.clear_temp_highlights()
                        #print(2, self.orgin_i, self.orgin_j)
                        self.temp_highlight_board[self.orgin_i][self.orgin_j] = GREEN
                        if i == self.orgin_i:
                            if j - self.orgin_j > 0:
                                for k in range(1, j - self.orgin_j + 1):
                                    self.temp_highlight_board[i][self.orgin_j + k] = GREEN
                            else:
                                for k in range(1, self.orgin_j - j + 1):
                                    self.temp_highlight_board[i][self.orgin_j - k] = GREEN

                            self.check_player_highlights()

                        elif j == self.orgin_j:
                            if i - self.orgin_i > 0:
                                for k in range(1, i - self.orgin_i + 1):
                                    self.temp_highlight_board[self.orgin_i + k][j] = GREEN
                            else:
                                for k in range(1, self.orgin_i - i + 1):
                                    self.temp_highlight_board[self.orgin_i - k][j] = GREEN

                            self.check_player_highlights()

                        elif self.orgin_i - self.orgin_j == i - j or self.orgin_i + self.orgin_j == i + j:
                            if i > self.orgin_i:
                                if j > self.orgin_j:
                                    for k in range(1, i - self.orgin_i + 1):
                                        self.temp_highlight_board[self.orgin_i + k][self.orgin_j + k] = GREEN
                                else:
                                    for k in range(1, i - self.orgin_i + 1):
                                        self.temp_highlight_board[self.orgin_i + k][self.orgin_j - k] = GREEN

                            else:
                                if i < self.orgin_i:
                                    if j > self.orgin_j:
                                        for k in range(1, self.orgin_i - i + 1):
                                            self.temp_highlight_board[self.orgin_i - k][self.orgin_j + k] = GREEN
                                    else:
                                        for k in range(1, self.orgin_i - i + 1):
                                            self.temp_highlight_board[self.orgin_i - k][self.orgin_j - k] = GREEN

                            self.check_player_highlights()
                        #self.highlight_board[i][j] = GREEN



        else:
            self.orgin_i = None
            self.orgin_j = None
            self.clear_temp_highlights()



    def refresh(self):
        screen.fill(WHITE)
        self.draw_word_list()
        self.draw_board()
        self.player_input()

    def solve(self):
        self.refresh()
        self.highlight.fill(RED)
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                for word in self.changing_word_list:
                    # if first letter correct
                    # check both directionss of horizontal, vertical, forward diagonal, backward diagonal
                    # list of 8 possible checks
                    # each letter of the word try to do the checks, whichever throw error or are wrong remove
                    # if the letter correct draw green box
                    # if reach end of loop, word is solved
                    if self.board[i][j] == word[0]:
                        self.highlight.fill(GREEN)
                        screen.blit(self.highlight, (j * self.offset + 200, i * self.offset))
                        #("letter: " + word[0] + " the first letter of " + word)
                        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                        # h, rh, v, rv, fd, rfd, bd, rbd

                        for k in range(1, len(word)):
                            #print(" for i in range " + str(len(directions)))
                            remove_list = []
                            for direction in directions:
                                try:
                                    if word[k] == self.board[i + (direction[1] * k)][j + (direction[0] * k)] and i + (direction[1] * k) >= 0 and j + (direction[0] * k) >= 0:
                                        if k == len(word) - 1:
                                            self.changing_word_list.remove(word)
                                            color = random_color()
                                            for l in range(len(word)):
                                                self.highlight_board[i + (direction[1] * l)][j + (direction[0] * l)] = color

                                        #print("letter: " + word[k] + " is in position " + str(j + (direction[0] * k)) + ", " + str(i + (direction[1] * k)) + " with h: " + str(direction[0]) + " and v: " + str(direction[1]))
                                        #print(directions)

                                        self.highlight.fill(GREEN)
                                        screen.blit(self.highlight, ((j + (direction[0] * k)) * self.offset + 200, (i + (direction[1] * k)) * self.offset))
                                        pygame.display.flip()
                                        time.sleep(self.time_delay * 5)
                                        #print(((j + (direction[0] * k)) * self.offset + 200, (i + (direction[1] * k)) * self.offset))

                                    elif i + (direction[1] * k) >= 0 and j + (direction[0] * k) >= 0:
                                        self.highlight.fill(YELLOW)
                                        screen.blit(self.highlight, ((j + (direction[0] * k)) * self.offset + 200, (i + (direction[1] * k)) * self.offset))
                                        pygame.display.flip()
                                        time.sleep(self.time_delay)
                                        #print("letter: " + word[k] + " is NOT in position " + str(j + (direction[0] * k)) + ", " + str(i + (direction[1] * k)) + " with h: " + str(direction[0]) + " and v: " + str(direction[1]))
                                        #print("letter " + self.board[i + (direction[1] * k)][j + (direction[0] * k)] + " was there...")
                                        #directions[directions.index(direction)] = (0,0)
                                        remove_list.append(direction)
                                        #print(directions)
                                except IndexError:
                                    #print("letter: " + word[k] + " gives an ERROR because " + str(j + (direction[0] * k)) + ", " + str(i + (direction[1] * k)) + " with h: " + str(direction[0]) + " and v: " + str(direction[1]))
                                    #[directions.index(direction)] = (0,0)
                                    remove_list.append(direction)
                                    #print(directions)
                            for item in remove_list:
                                directions.remove(item)

                    self.refresh()
                self.refresh()

                self.highlight.fill(RED)
                screen.blit(self.highlight, (j * self.offset + 200, i * self.offset))
                pygame.display.flip()
                time.sleep(self.time_delay)

        #print(changing_word_list)

class Button:
    def __init__(self, color, text, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.BUTTON_FONT = pygame.font.Font('freesansbold.ttf', 30)
        self.text_rect = self.BUTTON_FONT.render(self.text, True, BLACK)
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        # if the mouse goes over the button
        if self.rect.collidepoint(pos):
            # if we are clicking and the button is not clicked already, then set clicked to true
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True

        # if the mouse is not being pressed, set clicked to false
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(screen, self.color, self.rect)

        screen.blit(self.text_rect, (self.x + (self.width - self.text_rect.get_width()) // 2, self.y + self.text_rect.get_height() // 2))

        return action

class Menu:
    def __init__(self):
        self.selected = False

        self.input_font = pygame.font.Font(None, 100)
        self.input_text = '0  '
        self.input_box = pygame.Rect(600, 470, 160, 80)

        self.selected_color = (0, 0, 0)
        self.unselected_color = (145, 145, 145)
        self.used_color = self.unselected_color

        self.TITLE_FONT = pygame.font.Font('freesansbold.ttf', 75)
        self.TEXT_FONT = pygame.font.Font('freesansbold.ttf', 50)

        self.display_board = [['A', 'E', 'Z', 'G', 'L', 'D', 'B'],
                         ['Q', 'S', 'P', 'Y', 'C', 'A', 'O'],
                         ['N', 'U', 'M', 'B', 'E', 'R', 'U'],
                         ['O', 'F', 'H', 'T', 'V', 'M', 'G'],
                         ['W', 'O', 'R', 'D', 'S', '', ''],
                         ['E', 'F', 'M', 'O', 'S', 'I', 'S'],
                         ['10', '<', '=', 'N', '<', '=', '30']]

        self.highlight_board = [['', '', '', '', '', '', ''],
                              ['', '', '', '', '', '', ''],
                              [LIGHT_RED, LIGHT_RED, LIGHT_RED, LIGHT_RED, LIGHT_RED, LIGHT_RED, ''],
                              [BLUE, BLUE, '', '', '', '', ''],
                              [DARK_GREEN, DARK_GREEN, DARK_GREEN, DARK_GREEN, DARK_GREEN, '', ''],
                              ['', '', '', '', '', '', ''],
                              [PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE]]

        self.offset = 800 // 10
        self.highlight = pygame.Surface((self.offset, self.offset))
        self.highlight.set_alpha(128)

    def get_input(self):
        global word_search
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and self.selected:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-3]
                elif event.key == pygame.K_RETURN:
                    if self.input_text == '':
                        self.input_text = '0  '
                    elif int(''.join(self.input_text.split(' '))) > 30:
                        self.input_text = '3  0  '
                    elif int(''.join(self.input_text.split(' '))) < 10:
                        self.input_text = '1  0  '
                    else:
                        word_search = WordSearch(int(''.join(self.input_text.split(' '))))

                else:
                    if event.unicode.isdigit():
                        self.input_text += event.unicode + "  "

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(pygame.mouse.get_pos()):
                    self.selected = True
                    self.used_color = self.selected_color
                else:
                    self.selected = False
                    self.used_color = self.unselected_color

    def draw(self):
        screen.fill(WHITE)

        pygame.draw.rect(screen, LIGHT_RED, (0,0, SCREEN_WIDTH, 100))
        screen.blit(self.TITLE_FONT.render('WORD SEARCH SOLVER', True, BLACK), (50, 20))

        for i in range(7):
            for j in range(7):
                pygame.draw.rect(screen, GRAY, (j*self.offset + 200, i*self.offset + 150, self.offset, self.offset), 1)
                screen.blit(self.TEXT_FONT.render(self.display_board[i][j], True, BLACK), (j*self.offset + 200 + self.offset // 4, i*self.offset + self.offset // 4 + 150))

        for i in range(7):
            for j in range(7):
                if self.highlight_board[i][j] != '':
                    self.highlight.fill(self.highlight_board[i][j])
                    screen.blit(self.highlight, (j * self.offset + 200, i * self.offset + 150))

        #screen.blit(self.TEXT_FONT.render('NUMBER OF WORDS:', True, BLACK), (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3))

        pygame.draw.rect(screen, self.used_color, self.input_box, 2)
        input_surface = self.input_font.render(self.input_text, True, BLACK)
        screen.blit(input_surface, (self.input_box.x + 20, self.input_box.y + 7))
        self.input_box.w = max(160, input_surface.get_width() + 10)

#word_search = WordSearch()

menu = Menu()

solve_button = Button(YELLOW, "SOLVE", 0, 60, 200, 60)
reset_button = Button(RED, "RESET", 0, 120, 200, 60)
generate_button = Button(GREEN, "GENERATE", 0, 0, 200, 60)
menu_button = Button(BLUE, "MENU", 0, 180, 200, 60)

def main():
    if started:
        word_search.refresh()
        word_search.player_input()
    else:
        menu.get_input()
        menu.draw()

    pygame.display.flip()
    clock.tick(60)

while True:
    main()


