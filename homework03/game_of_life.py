import pygame
import random
from pygame.locals import *
from pprint import pprint as pp


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 1):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed


    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list()
            self.update_cell_list()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        grid = []
        if (randomize):
            for i in range(0, self.cell_height):
                col = []
                for j in range(0, self.cell_width):
                    col.append(random.randint(0,1))
                grid.append(col);
        self.grid = grid

    def draw_cell_list(self):
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                x = i * self.cell_size + 1
                y = j * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))

    def get_neighbours(self, cell):
        neighbours = 0
        x, y = cell
        n = self.cell_height - 1
        m = self.cell_width - 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (i >= 0 and i <= n and j >= 0 and j <= m) or (i == x and j == y):
                    continue
                if self.grid[i][j]:
                    neighbours += 1
        return neighbours

    def update_cell_list(self):
        new_grid = self.grid
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                cnt = self.get_neighbours((i, j))
                if not (2 <= cnt and cnt <= 3):
                    new_grid[i][j] = 0
        self.grid = new_grid
    


if __name__ == '__main__':
    game = GameOfLife(1280, 960, 10)
    game.cell_list(randomize=True)
    game.run()