import random
import evolutive
import math


def fitness2(cromozom, board):
    score = 0
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
                if cromozom[i][j] != 0:
                    score += 1
    return score


def fitness1(cromozom, board):
    score = 0
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == 0:
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
    return score


def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0, len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 1e16
    distance[len(front) - 1] = 1e16
    val = max(values1) - min(values1)
    if val == 0:
        val = 1e-9
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / val
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / val
    return distance


def fast_non_dominated_sort(values1, values2):
    S = [[] for i in range(0, len(values1))]
    front = [[]]
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                    values1[p] >= values1[q] and values2[p] > values2[q]) or (
                    values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                    values1[q] >= values1[p] and values2[q] > values2[p]) or (
                    values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while front[i] != []:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]
    return front


def Selection(cromozomi, board):
    function1_values = [fitness1(cromozomi[i], board) for i in range(0, len(cromozomi))]
    function2_values = [fitness2(cromozomi[i], board) for i in range(0, len(cromozomi))]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
    crowding_distance_values = []
    newCromozomi = []
    for i in range(0, len(non_dominated_sorted_solution)):
        crowding_distance_values.append(
            crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
    for i in range(0, len(non_dominated_sorted_solution)):
        non_dominated_sorted_solution2_1 = [
            index_of(non_dominated_sorted_solution[i][j], non_dominated_sorted_solution[i]) for j in
            range(0, len(non_dominated_sorted_solution[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values[i][:])
        front = [non_dominated_sorted_solution[i][front22[j]] for j in
                 range(0, len(non_dominated_sorted_solution[i]))]
        front.reverse()
        for value in front:
            newCromozomi.append(value)
            if len(newCromozomi) == evolutive.population:
                break
        if len(newCromozomi) == evolutive.population:
            break
    return [cromozomi[i] for i in newCromozomi]


def NSGA2(cromozomi, board):
    newcromozomi = evolutive.Incrucisare(cromozomi)
    newcromozomi2 = evolutive.Mutation(cromozomi, board)
    for i in newcromozomi2:
        newcromozomi += [i]
    cromozomi = Selection(newcromozomi, board)

    function1_values = [fitness1(cromozomi[i], board) for i in range(0, len(cromozomi))]
    function2_values = [fitness2(cromozomi[i], board) for i in range(0, len(cromozomi))]
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
    crowding_distance_values = []
    for i in range(0, len(non_dominated_sorted_solution)):
        crowding_distance_values.append(
            crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
    return cromozomi, non_dominated_sorted_solution

