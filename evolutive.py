import random

population = 100
sansa = 0.5
sansa_selectie = 0.5
sansa_mutatie = 0.1
nr_modificari_mutatie = 30


def generateNumber():
    sansa = 1
    x = random.random()
    if x < sansa:
        return random.randint(0, 9)
    else:
        return 0


def generateCromozoms(board):
    global population
    cromozomi = []
    for _ in range(0, population):
        newsMat = []
        for line in board:
            row = []
            for element in line:
                if element == 0:
                    number = generateNumber()
                    row += [number]
                else:
                    row += [element]
            newsMat += [row]
        cromozomi += [newsMat]
    return cromozomi


def fitness(cromozom, board):
    score = 0
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
                if cromozom[i][j] == 0:
                    score -= 10
                else:
                    bun = True
                    patratx, patraty = j // 3 * 3, i // 3 * 3

                    for y in range(0, 3):
                        for x in range(0, 3):
                            if cromozom[patraty + y][patratx + x] == cromozom[i][j] and not (
                                    patraty + y == i and patratx + x == j):
                                bun = False
                    for x in range(0, 9):
                        if x != j and cromozom[i][x] == cromozom[i][j]:
                            bun = False
                        if x != i and cromozom[x][j] == cromozom[i][j]:
                            bun = False
                    if bun:
                        score += 10
                    else:
                        score -= 50
    return score


def Incrucisare(cromozoms):
    newCromozomi = []
    for index, i in enumerate(cromozoms):
        newCromozomi += [i]
        x = random.random()
        if x < sansa:
            index2 = random.randint(0, len(cromozoms) - 1)
            while index == index2:
                index2 = random.randint(0, len(cromozoms) - 1)
            j = cromozoms[index2]
            newCromozom = []
            for pozy in range(0, len(i)):
                newC = []
                for pozx in range(0, len(i[pozy])):
                    x = random.random()
                    if x < sansa_selectie:
                        newC += [i[pozy][pozx]]
                    else:
                        newC += [j[pozy][pozx]]
                newCromozom += [newC]
            newCromozomi += [newCromozom]
    return newCromozomi


def Mutation2(cromozoms, board):
    newCromozomi = []
    for i in cromozoms:
        newC = i.copy()
        for pozy in range(0, len(i)):
            for pozx in range(0, len(i[pozy])):
                if board[pozy][pozx] != 0:
                    t = random.random()
                    if t < sansa_mutatie:
                        newC[pozy][pozx] = generateNumber()
        newCromozomi += [newC]
    return newCromozomi


def Mutation(cromozoms, board):
    newCromozomi = []
    for i in cromozoms:
        t = random.random()
        if t < sansa_mutatie:
            for _ in range(0, nr_modificari_mutatie):
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                while board[y][x] != 0:
                    x = random.randint(0, 8)
                    y = random.randint(0, 8)
                i[y][x] = generateNumber()
            newCromozomi += [i]
    return newCromozomi

def Mutation3(cromozoms, board):
    newCromozomi = []
    for i in cromozoms:
        for x in range(len(i)):
            for y in range(len(i[x])):
                if board[y][x] == 0:
                    t = random.random()
                    if t < sansa_mutatie:
                        for _ in range(0, nr_modificari_mutatie):
                            newValue = random.randint(0, 8)
                            while board[y][x] != 0:
                                newValue = random.randint(0, 8)
                            i[y][x] = newValue
                        newCromozomi += [i]
    return newCromozomi


def Selection(cromozoms, board):
    newCromozomi = []
    while len(newCromozomi) < population:
        index = random.randint(0, len(cromozoms) - 1)
        i = cromozoms[index]
        index2 = random.randint(0, len(cromozoms) - 1)
        while index == index2:
            index2 = random.randint(0, len(cromozoms) - 1)
        j = cromozoms[index2]
        if fitness(i, board) > fitness(j, board):
            newCromozomi += [i]
            cromozoms.remove(i)
        else:
            newCromozomi += [j]
            cromozoms.remove(j)
    return newCromozomi


def EVOLUTIVE(cromozomi, board):
    newcromozomi = Incrucisare(cromozomi)
    newcromozomi2 = Mutation(cromozomi, board)
    for i in newcromozomi2:
        newcromozomi += [i]
    cromozomi = Selection(newcromozomi, board)
    cromozomi = sorted(cromozomi, key=lambda cromozom: fitness(cromozom, board), reverse=True)
    return cromozomi
