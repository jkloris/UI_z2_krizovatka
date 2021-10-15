import copy
import random

GRID_SIZE = 6
GATE = 2
RED_ID = 1

class Uzol:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.grid = Grid(state)

    def checkFin(self):
        red_i = [i for i in self.state if i.id == RED_ID][0]
        for i in range(red_i.col + red_i.size,GRID_SIZE):
            if self.grid.table[GATE][i] == 1:
                return False
        return True

#id je od 0
class Car:
    def __init__(self, id, size, line, col, direct):
        self.col = col
        self.line = line
        self.direct = direct
        self.size = size
        self.id = id

    def moveLeft(self, grid):
        if self.direct == 'h' and self.col > 0 and grid.table[self.line][self.col-1] == 0:
            grid.table[self.line][self.col - 1] = 1
            grid.table[self.line][self.col + self.size-1] = 0
            self.col-=1
            return True
        return False

    def moveRight(self, grid):
        if self.direct == 'h' and self.col + self.size < GRID_SIZE and grid.table[self.line][self.col + self.size] == 0:
            grid.table[self.line][self.col + self.size] = 1
            grid.table[self.line][self.col] = 0
            self.col += 1
            return True
        return False

    def moveUp(self, grid):
        if self.direct == 'v' and self.line > 0 and grid.table[self.line-1][self.col] == 0:
            grid.table[self.line-1][self.col] = 1
            grid.table[self.line+ self.size - 1][self.col ] = 0
            self.line -= 1
            return True
        return False

    def moveDown(self, grid):
        if self.direct == 'v' and self.line + self.size < GRID_SIZE and grid.table[self.line + self.size][self.col] == 0:
            grid.table[self.line + self.size][self.col] = 1
            grid.table[self.line][self.col] = 0
            self.line += 1
            return True
        return False

class Grid:
    def __init__(self, state):
        self.table = []
        for y in range(GRID_SIZE):
            self.table.append([])
            for x in range(GRID_SIZE):
                self.table[y].append(0)

        for car in state:
            for i in range(car.size):
                if car.direct == 'h':
                    self.table[car.line][car.col + i] = 1
                    continue
                if car.direct == 'v':
                    self.table[car.line + i][car.col] = 1


    def printGrid(self):
        for y in range(GRID_SIZE):
            self.table.append([])
            s=''
            for x in range(GRID_SIZE):
                s+=str(self.table[y][x]) + ' '
            print(s)

class IterativeDeepSearch:
    queue = []

    def __init__(self, uzol):
        self.uzol = uzol

    def doOneIteration(self):
            pass

def depthSearch(uzol,limit):
    if limit <= 0:
        return False

    if uzol.checkFin():
        print()
        uzol.grid.printGrid()
        return True
    random.shuffle(uzol.state)
    for car in range(len(uzol.state)):
        uzolCpy = copy.deepcopy(uzol)
        uzolCpy.parent = uzol
        if uzolCpy.state[car].moveLeft(uzolCpy.grid):
            if uzolCpy.grid.table != uzol.parent.grid.table:
                if depthSearch(uzolCpy, limit-1): return True
        uzolCpy = copy.deepcopy(uzol)
        uzolCpy.parent = uzol
        if uzolCpy.state[car].moveRight(uzolCpy.grid):
            if uzolCpy.grid.table != uzol.parent.grid.table:
                if depthSearch(uzolCpy, limit-1): return True
        uzolCpy = copy.deepcopy(uzol)
        uzolCpy.parent = uzol
        if uzolCpy.state[car].moveUp(uzolCpy.grid):
            if uzolCpy.grid.table != uzol.parent.grid.table:
                if depthSearch(uzolCpy, limit-1): return True
        uzolCpy = copy.deepcopy(uzol)
        uzolCpy.parent = uzol
        if uzolCpy.state[car].moveDown(uzolCpy.grid):
            if uzolCpy.grid.table != uzol.parent.grid.table:
                if depthSearch(uzolCpy, limit-1): return True
    # print()
    # uzol.grid.printGrid()
    return False

def main():
    states = []
    # states.append(Car(6, 2, 5, 2, 'h'));
    # states.append(Car(5, 3, 1, 3, 'v'));
    # states.append(Car(8, 3, 2, 5, 'v'));
    # states.append(Car(1, 2, 2, 1, 'h'));
    # states.append(Car(2, 2, 0, 0, 'h'));
    # states.append(Car(3, 3, 1, 0, 'v'));
    # states.append(Car(4, 2, 4, 0, 'v'));
    # states.append(Car(7, 2, 4, 1, 'h'));

    states.append(Car(1, 2, 2, 1, 'h'));
    states.append(Car(2, 2, 0, 0, 'h'));
    states.append(Car(3, 3, 1, 0, 'v'));
    states.append(Car(4, 2, 4, 0, 'v'));
    states.append(Car(5, 3, 1, 3, 'v'));
    states.append(Car(6, 2, 5, 2, 'h'));
    states.append(Car(7, 2, 4, 1, 'h'));
    states.append(Car(8, 3, 2, 5, 'v'));

    hlUzol = Uzol(states, None)
    hlUzol.parent = hlUzol
    hlUzol.grid.printGrid()

    depthSearch(hlUzol,5)





if __name__ == "__main__":
    main()
