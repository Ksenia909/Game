from random import sample


class Cell:
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.number = 0
        self.is_open = False
        self.is_flag = False


class GamePole:
    INDX = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self, size_n, size_m, total_mines, level):
        self.size_n = size_n
        self.size_m = size_m
        self.total_mines = total_mines
        self.start = True
        self.mines = None
        self.pole = None
        self.level = level

    def init_pole(self, num):
        w, h, total_mines = self.size_m, self.size_n, self.total_mines
        x = [i for i in range(w*h) if i != num]
        self.mines = sample(x, total_mines)

        pole = tuple(tuple(Cell(True) if w * n - w + m in self.mines else Cell() for m in range(w))
                     for n in range(1, h + 1))

        for n in range(h):
            for m in range(w):
                if pole[n][m].is_mine:
                    for i, j in self.INDX:
                        if 0 <= n + i < h and 0 <= m + j < w:
                            pole[n + i][m + j].number += 1

        self.pole = pole



