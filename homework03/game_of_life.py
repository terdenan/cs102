import pygame
import random
from pygame.locals import *
from pprint import pprint as pp


class Cell:
    def __init__(self, alive):
        self.alive = bool(alive)

    def is_alive(self):
        return self.alive


class CellList:
    def __init__(self, cell_width, cell_height, randomize=False, filename=""):
        self.cell_width = cell_width
        self.cell_height = cell_height
        if (randomize):
            self.grid = [[Cell(random.randint(0, 1))
                          for i in range(cell_width)]
                         for j in range(cell_height)]
        else:
            fileData = [c for c in open(filename).read() if c in '01']
            grid = []
            for i in range(cell_height):
                col = []
                for j in range(cell_width):
                    symbol = int(fileData[i*cell_width+j])
                    col.append(Cell(symbol))
                grid.append(col)
            self.grid = grid

    def get_neighbours(self, cell):
        neighbours = 0
        x, y = cell
        n = self.cell_height - 1
        m = self.cell_width - 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (0 <= i <= n and 0 <= j <= m) or (i == x and j == y):
                    continue
                if self.grid[i][j].is_alive():
                    neighbours += 1
        return neighbours

    def update(self):
        new_grid = self.grid
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                cnt = self.get_neighbours((i, j))
                if not (2 <= cnt and cnt <= 3):
                    new_grid[i][j].alive = False
        self.grid = new_grid

    def __iter__(self):
        self.i_cnt, self.j_cnt = 0, 0
        return self

    def __next__(self):
        cell = self.grid[self.i_cnt][self.j_cnt]
        self.j_cnt += 1
        self.i_cnt += self.j_cnt // self.cell_width
        self.j_cnt //= self.cell_width
        if (self.i_cnt == self.cell_height):
            raise StopIteration
        else:
            return cell

    def __str__(self):
        return "Экземпляр объекта CellList"


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=1):
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
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (
                x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (
                0, y), (self.width, y))

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
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False, filename=""):
        self.clist = CellList(self.cell_width, self.cell_height,
                              randomize, filename)
        self.grid = self.clist.grid

    def draw_cell_list(self):
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.grid[i][j].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                        x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (
                        x, y, a, b))


if __name__ == '__main__':
    game = GameOfLife(320, 240, 40)
    game.cell_list(randomize=True, filename="test.txt")
    game.run()
