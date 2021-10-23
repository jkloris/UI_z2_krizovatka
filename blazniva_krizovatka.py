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

def printFinish(me):
    while me != None:
        me.grid.printGrid()
        me = me.parent
    return True

def depthSearch(uzolStart,limit):
    tmpCounter = 0
    uzolTime = 0
    otherTime = time.time()

    front = [[uzolStart, limit]]
    while len(front) > 0:
        if front[0][0].checkFin():
            print(tmpCounter)
            printFinish(front[0][0])
            return True

        uzol = front.pop(0)
        tmpCounter+=1

        #uzol[0] == samotny uzol, uzol[1] je limit
        if uzol[1] < 0: continue

        random.shuffle(uzol[0].state)

        for car in range(len(uzol[0].state)):

            start = time.time()
            uzolCpy = Uzol(uzol[0].state, uzol[0])
            uzolCpy.grid = Grid(uzol[0].grid.table, "Table")
            uzolCpy2 = Uzol(uzol[0].state, uzol[0])
            uzolCpy2.grid = Grid(uzol[0].grid.table, "Table")
            uzolTime += time.time()-start

            if uzol[0].state[car].direct == 'v':

                while uzolCpy.state[car].moveDown(uzolCpy.grid):
                    if checkParent(uzolCpy):
                        front.insert(0, [uzolCpy, uzol[1] - 1])

                while uzolCpy2.state[car].moveUp(uzolCpy2.grid):
                    if checkParent(uzolCpy2):
                        front.insert(0, [uzolCpy2, uzol[1] - 1])

            elif uzol[0].state[car].direct == 'h':

                while uzolCpy.state[car].moveLeft(uzolCpy.grid):
                    if checkParent(uzolCpy):
                        front.insert(0, [uzolCpy, uzol[1] - 1])

                while uzolCpy2.state[car].moveRight(uzolCpy2.grid):
                    if checkParent(uzolCpy2):
                        front.insert(0, [uzolCpy2, uzol[1] - 1])




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
    # states.append(Car(2, 2, 0, 0, 'h'));
    # states.append(Car(3, 3, 1, 0, 'v'));
    # states.append(Car(4, 2, 4, 0, 'v'));
    # states.append(Car(5, 3, 1, 3, 'v'));
    # states.append(Car(6, 2, 5, 2, 'h'));
    # states.append(Car(7, 2, 4, 1, 'h'));
    # states.append(Car(8, 3, 2, 4, 'v'));

    #vzorovy
    states.append(Car(1, 2, 2, 1, 'h'));
    states.append(Car(2, 2, 0, 0, 'h'));
    states.append(Car(3, 3, 1, 0, 'v'));
    states.append(Car(4, 2, 4, 0, 'v'));
    states.append(Car(5, 3, 1, 3, 'v'));
    states.append(Car(6, 3, 5, 2, 'h'));
    states.append(Car(7, 2, 4, 4, 'h'));
    states.append(Car(8, 3, 0, 5, 'v'));



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

    a = Uzol(hlUzol.state, hlUzol)
    a.grid = Grid(hlUzol.grid.table, "Table")

    a.state[1].moveRight(a.grid)
    # depthSearch(hlUzol,4)
    print("")
    search = IterativeDeepSearch(hlUzol)




if __name__ == "__main__":
    main()

