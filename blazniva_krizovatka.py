import time
import random


GRID_SIZE = 6
GATE = 2
RED_ID = 1

class Uzol:
    def __init__(self, state, parent):
        self.state = self.copyState(state)
        self.parent = parent
        self.grid = None

    def checkFin(self):
        for i in self.state:
            if i.id == RED_ID:
                red_i = i
                break

        for i in range(red_i.col + red_i.size,GRID_SIZE):
            if self.grid.table[GATE][i] == 1:
                return False
        return True

    def copyState(self, state):
        thisState = []
        for i in state:
            thisState.append(Car(i.id, i.size, i.line, i.col, i.direct))
        return thisState

    def recreateGrid(self, seq):
        table = []
        offset = len(self.state)*[0]
        for y in range(GRID_SIZE):
            table.append(self.grid.table[y][:])

        for step in seq:
            if type(step) == int:
                return [table, offset]
            car = int(step[0])

            if step[1] == 'R':
                moveRight(self.state[car], table, offset[car])
                offset[car]+=1
                continue
            elif step[1] == 'L':
                moveLeft(self.state[car], table, offset[car])
                offset[car] -= 1
                continue
            elif step[1] == 'D':
                moveDown(self.state[car], table, offset[car])
                offset[car] += 1
                continue
            elif step[1] == 'U':
                moveUp(self.state[car], table, offset[car])
                offset[car] -= 1
                continue




#id je od 0
class Car:
    def __init__(self, id, size, line, col, direct):
        self.col = col
        self.line = line
        self.direct = direct
        self.size = size
        self.id = id

    def __cmp__(self, other):
        if self.col == other.col and self.line == other.line and self.direct == other.direct and self.size == other.size and self.id == other.id:
            return 0
        return 1

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

def moveLeft(car, table, offset):
    table[car.line][car.col+ offset - 1 ] = 1
    table[car.line][car.col + offset + car.size-1] = 0

def moveRight(car, table, offset):
    table[car.line][car.col + offset + car.size] = 1
    table[car.line][car.col + offset] = 0

def moveUp(car, table, offset):
    table[car.line + offset - 1][car.col] = 1
    table[car.line + offset + car.size - 1][car.col] = 0

def moveDown(car, table, offset):
    table[car.line + offset + car.size][car.col] = 1
    table[car.line + offset][car.col] = 0


def checkLeft(car, table, offset):
    if car.direct == 'h' and car.col + offset > 0 and table[car.line][car.col + offset - 1] == 0:
        return True
    return False

def checkRight(car, table, offset):
    if car.direct == 'h' and car.col + offset + car.size < GRID_SIZE and table[car.line][car.col + offset + car.size] == 0:
        return True
    return False

def checkUp(car, table, offset):
    if car.direct == 'v' and car.line + offset > 0 and table[car.line + offset - 1][car.col] == 0:
        return True
    return False

def checkDown(car, table, offset):
    if car.direct == 'v' and car.line + offset + car.size < GRID_SIZE and table[car.line + offset + car.size][car.col] == 0:
        return True
    return False

class Grid:
    def __init__(self, item, flag):
        self.table = []
        if flag == "State":
            self.createGrid(item)
        elif flag == "Table":
            self.copyGrid(item)

    def copyGrid(self, table):
        for y in range(GRID_SIZE):
            self.table.append(table[y][:])

    def createGrid(self, state):
        for y in range(GRID_SIZE):
            self.table.append([])
            self.table[y] = GRID_SIZE * [0]

        for car in state:
            for i in range(car.size):
                if car.direct == 'h':
                    self.table[car.line][car.col + i] = 1
                    continue
                if car.direct == 'v':
                    self.table[car.line + i][car.col] = 1
        return

    def printGrid(self):
        for y in range(GRID_SIZE):
            s=''
            for x in range(GRID_SIZE):
                s+=str(self.table[y][x]) + ' '
            print(s)
        print()




class IterativeDeepSearch:

    def __init__(self, uzol):
        self.uzol = uzol
        self.limit = 0

        while not depthSearch(self.uzol, self.limit):
            print(f"Hlbka {self.limit + 1} prehladana")
            self.limit+=1

def checkParent(me):
    parent = me.parent
    while parent != None:
        if me.grid.table == parent.grid.table:
            return False
        parent = parent.parent
    return True

def checkParent2(seq, offset):
    parent = seq[:]
    offsetCpy = offset[:]
    while len(parent)>1:
        if offsetCpy == offset and len(parent) != len(seq):
            return False
        a = parent.pop(-2)
        car = int(a[0])
        if a[1] == 'R':
            offsetCpy[car]-=1
            continue
        elif a[1] == 'L':
            offsetCpy[car]+=1
            continue
        elif a[1] == 'U':
            offsetCpy[car]+=1
            continue
        elif a[1] == 'D':
            offsetCpy[car]-=1
            continue
    if offsetCpy == offset:
        return False
    return True


def checkFin(table, red_i, offset):
    for i in range(red_i.col + offset + red_i.size, GRID_SIZE):
        if table[GATE][i] == 1:
            return False
    return True

def printFinish(me):
    while me != None:
        me.grid.printGrid()
        me = me.parent
    return True

def depthSearch(uzolStart,limit):
    tmpCounter = 0
    uzolTime = 0
    otherTime = time.time()

    front2 = [[limit]]
    while len(front2) > 0:

        rad = front2.pop(0)
        tmpCounter+=1

        cpyTable, offset = uzolStart.recreateGrid(rad)
        if checkFin(cpyTable, uzolStart.state[0], offset[0]):
            print(rad)
            return True
        if rad[-1] < 0:  continue

        for car in range(len(uzolStart.state)):


            copy1 = rad[:]
            copy2 = rad[:]


            if uzolStart.state[car].direct == 'v':

                if checkDown(uzolStart.state[car], cpyTable, offset[car]):
                    copy1.insert(-1, f"{car}D")
                    if checkParent2(copy1, offset):
                        copy1[-1] = copy1[-1] - 1
                        front2.insert(0, copy1)


                if checkUp(uzolStart.state[car], cpyTable, offset[car]):
                    copy2.insert(-1, f"{car}U")
                    if checkParent2(copy2, offset):
                        copy2[-1] = copy2[-1] - 1
                        front2.insert(0, copy2)

            elif uzolStart.state[car].direct == 'h':

                if checkLeft(uzolStart.state[car], cpyTable, offset[car]):
                    copy1.insert(-1, f"{car}L")
                    if checkParent2(copy1, offset):
                        copy1[-1] = copy1[-1] - 1
                        front2.insert(0, copy1)

                if checkRight(uzolStart.state[car], cpyTable, offset[car]):
                    copy2.insert(-1, f"{car}R")
                    if checkParent2(copy2, offset):
                        copy2[-1] = copy2[-1] - 1
                        front2.insert(0, copy2)

    print(tmpCounter, uzolTime, time.time()-otherTime-uzolTime)
    copyTime = 0
    return False


# class Hash:
#
#
#     def __init__(self):
#         self.plnka = 0
#         self.hashTable = [None] * 1001
#
#     def getHash(self, state):
#         x = 0
#         for car in state:
#             x += (car.col + car.line*37 + ord(car.direct) ) * state.index(car)*car.size
#
#         return x % len(self.hashTable)
#
#     # returns True if state1 == state2
#     def cmpState(self, state1, state2):
#         for i in range(len(state1)):
#             if state1[i] != state2[i]:
#                 return False
#         return True
#
#
#
#     def addState(self, state):
#         x = self.getHash(state)
#
#         while self.hashTable[x] != None:
#             if self.cmpState(self.hashTable[x], state):
#                 print("Zhoda")
#                 return False
#             x = x+1 if x<len(self.hashTable)-1 else 0
#
#         self.hashTable[x] = state
#         self.plnka+=1
#
#         if self.plnka / len(self.hashTable) > 0.5:
#             self.rehash()
#         return True
#
#     def rehash(self):
#         tmpTable = [None] * len(self.hashTable)*2
#         for i in self.hashTable:
#             if i == None:
#                 continue
#             x = self.getHash(i)
#             while tmpTable[x] != None:
#                 x = x + 1 if x < len(tmpTable) - 1 else 0
#
#             tmpTable[x] = i
#
#         self.hashTable = tmpTable


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

    # states.append(Car(1, 2, 2, 1, 'h'));
    # states.append(Car(2, 3, 0, 0, 'v'));
    # states.append(Car(3, 2, 3, 0, 'v'));
    # states.append(Car(4, 2, 5, 0, 'h'));
    # states.append(Car(5, 2, 1, 3, 'v'));
    # states.append(Car(6, 3, 0, 1, 'h'));
    # states.append(Car(7, 4, 4, 1, 'h'));
    # states.append(Car(8, 3, 0, 5, 'v'));

    #vzorovy
    states.append(Car(1, 2, 2, 1, 'h'));
    states.append(Car(2, 2, 0, 0, 'h'));
    states.append(Car(3, 3, 1, 0, 'v'));
    states.append(Car(4, 2, 4, 0, 'v'));
    states.append(Car(5, 3, 1, 3, 'v'));
    states.append(Car(6, 3, 5, 2, 'h'));
    states.append(Car(7, 2, 4, 4, 'h'));
    # states.append(Car(8, 3, 0, 5, 'v'));



    # states.append(Car(1, 2, 2, 1, 'h'));
    # states.append(Car(2, 2, 0, 0, 'h'));
    # states.append(Car(3, 3, 1, 0, 'v'));
    # states.append(Car(4, 2, 4, 0, 'v'));
    # states.append(Car(5, 3, 1, 3, 'v'));
    # states.append(Car(6, 3, 5, 2, 'h'));
    # states.append(Car(7, 2, 4, 4, 'h'));
    # states.append(Car(8, 3, 0, 5, 'v'));
    # states.append(Car(9, 2, 0, 4, 'v'));

    hlUzol = Uzol(states, None)
    hlUzol.grid = Grid(states, "State")
    hlUzol.parent = None
    hlUzol.grid.printGrid()

    start = time.time()
    search = IterativeDeepSearch(hlUzol)
    print(f"Celkovy cas hladania: {time.time() - start}")



if __name__ == "__main__":
    main()

