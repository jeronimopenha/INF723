import sys

import pygame


class Visu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Define the colors we will use in RGB format
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        pygame.init()
        self.win = pygame.display.set_mode()
        # TODO VER ESSE CAPTION DA JANELA
        w, h = self.win.get_size()
        self.screen_width = w * 90 // 100
        self.screen_height = h * 90 // 100
        self.win =pygame.display.set_mode((self.screen_width,self.screen_height))
        self.user_width = self.screen_width * 95 // 100
        self.user_height = self.screen_height * 95 // 100

    def update_window(self):
        pygame.display.set_caption('Visualização de dados')
        self.win.fill(self.WHITE)
        # drawing the separators lines
        i_x = 0 + ((self.screen_width - self.user_width) // 2)
        i_y = 0 + ((self.screen_height - self.user_height) // 2)
        e_x = self.user_width + ((self.screen_width - self.user_width) // 2)
        e_y = self.user_height + ((self.screen_height - self.user_height) // 2)
        # horizontal top line
        pygame.draw.line(self.win, self.BLACK, [i_x, i_y], [ e_x,i_y], 1)
        # horizontal bot line
        pygame.draw.line(self.win, self.BLACK, [i_x, e_y], [ e_x,e_y], 1)
        # vertical left line
        pygame.draw.line(self.win, self.BLACK, [i_x, i_y], [ i_x,e_y], 1)
        #  vertical right line
        pygame.draw.line(self.win, self.BLACK, [e_x, i_y], [ e_x,e_y], 1)

        # dividing the plot area, the filter area and the emphasis area
        # main box
        i_x = 0 + ((self.screen_width - self.user_width) // 2) + (80*self.user_width//100)
        pygame.draw.line(self.win, self.BLACK, [i_x, i_y], [i_x, e_y], 1)

        # Update the window
        pygame.display.flip()

    # todo ing
    def exec(self):
        print(self.screen_width, self.screen_height)
        while 1:
            self.update_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

    # todo
    def read_db(self):
        pass


v = Visu()
v.exec()

'''
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
'''
