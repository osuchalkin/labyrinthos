import pygame as pg
import random

# Starting maze - Knossos' Labyrinthos
_ = False
lab_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, 1, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1],
    [1, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, _, _, 1, _, _, 1, _, _, _, 1, _, _, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, _, _, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, _, 1],
    [1, _, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1, _, 1],
    [1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
    [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.level = game.level
        if self.level == 0:
            self.game_map = lab_map
            self.start = (1, 1)
            self.finish = (11, 14)
        else:
            self.size = self.level + 8  # for building random maze
            self.game_map, self.start, self.finish = self.get_maze()
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.game_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw2d(self):
        size = int(self.settings.HEIGHT / len(self.game_map))
        [pg.draw.rect(self.game.screen, 'darkgrey', (pos[0] * size, pos[1] * size, size, size), 2)
         for pos in self.world_map]
        return size

    @staticmethod
    def start_point_generate(n, m):
        """Starting point of the maze"""
        if random.choice([True, False]):
            if random.choice([True, False]):
                start = (0, random.randint(0, m - 1))
            else:
                start = (n - 1, random.randint(0, m - 1))
        else:
            if random.choice([True, False]):
                start = (random.randint(0, n - 1), 0)
            else:
                start = (random.randint(0, n - 1), m - 1)
        return start

    @staticmethod
    def transition_choice(x, y, rm):
        """Building a path in a maze"""
        choice_list = []
        if x > 0:
            if not rm[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if not rm[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not rm[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if not rm[x][y + 1]:
                choice_list.append((x, y + 1))
        if choice_list:
            nx, ny = random.choice(choice_list)
            if x == nx:
                if ny > y:
                    tx, ty = x * 2, ny * 2 - 1
                else:
                    tx, ty = x * 2, ny * 2 + 1
            else:
                if nx > x:
                    tx, ty = nx * 2 - 1, y * 2
                else:
                    tx, ty = nx * 2 + 1, y * 2
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1

    def create_labyrinth(self, n=5, m=5):
        """Maze generation"""
        reach_matrix = []
        for i in range(n):  # create a cell reachability matrix
            reach_matrix.append([])
            for j in range(m):
                reach_matrix[i].append(False)
        transition_matrix = []
        for i in range(n * 2 - 1):  # filling the transition matrix
            transition_matrix.append([])
            for j in range(m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    transition_matrix[i].append(0)  # way
                else:
                    transition_matrix[i].append(1)  # wall

        start = self.start_point_generate(n, m)

        list_transition = [start]
        x, y = start
        reach_matrix[x][y] = True
        x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
        for i in range(1, m * n):
            while not (x >= 0 and y >= 0):
                x, y = list_transition[-1]
                list_transition.pop()
                x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
            reach_matrix[x][y] = True
            list_transition.append((x, y))
            transition_matrix[tx][ty] = 0  # way
            x, y, tx, ty = self.transition_choice(x, y, reach_matrix)

        return transition_matrix

    @staticmethod
    def get_start(lab):
        """Start point"""
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, len(lab[0]) - 1)
            if lab[x][y] == 0:
                return x, y

    @staticmethod
    def get_finish(lab):
        """Finish point"""
        while True:
            x = random.randint(len(lab) - 3, len(lab) - 1)
            y = random.randint(0, len(lab[0]) - 1)
            if lab[x][y] == 0:
                return x, y

    def build_walls(self, maze):
        """Building walls around the maze"""
        width = len(maze) + 2
        height = len(maze[0]) + 2
        lab = [[1] * width for _ in range(height)]

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                lab[i + 1][j + 1] = maze[i][j]

        # start & finish
        start = self.get_start(lab)
        finish = self.get_finish(lab)

        # the wall N 3 (with secrets)
        i = 0
        while i < self.level and i < 3:
            x = random.randint(0, len(lab)-1)
            y = random.randint(0, len(lab)-1)
            if lab[x][y] == 1:
                lab[x][y] = 3
                i += 1

        return lab, start, finish

    def get_maze(self):
        matrix = self.create_labyrinth(self.size, self.size)
        return self.build_walls(matrix)


class MapSaved(Map):
    def __init__(self, game, level, game_map, start, finish):
        super().__init__(game)
        self.level = level
        self.game_map = game_map
        self.start = start
        self.finish = finish

        self.world_map = {}
        self.get_map()
