import random

import pygame
import json
import time

import evolutive
import NSGA2
import numpy as np

WIDTH = 740
HEIGHT = 740
first = True
background_color = (251, 247, 245)
element_color = (52, 31, 151)
board = []
buff = 17
player = False
use_nsga = True
cromozomi = []


def import_board_sudoku(filename):
    with open(filename, 'r') as f:
        mat = json.load(f)
    return mat


def winGame(mat):
    win = True
    for i in range(len(mat)):
        # se verifica liniile
        if len(set(mat[i])) != 9:
            win = False
        # se verifica coloanele
        if len(set([mat[j][i] for j in range(9)])) != 9:
            win = False
        for j in range(len(mat[0])):
            # se verifica sa fie completate toate elementele
            if mat[i][j] == 0:
                win = False

    # se verifica patratele 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if len(set([mat[x][y] for x in range(i, i + 3) for y in range(j, j + 3)])) != 9:
                win = False

    return win


def insertValue(win, position):
    myFont = pygame.font.SysFont('Comic Sans MS', 45)
    x, y = position[1], position[0]

    while True:
        for E in pygame.event.get():
            if E.type == pygame.QUIT:
                return
            if E.type == pygame.KEYDOWN:
                if board[x - 1][y - 1] != 0:
                    return

                if E.key - 48 == 0:  # verific valoarea daca se apasa tasta 0 pentru a sterge valaorea din sMat
                    sMat[x - 1][y - 1] = 0
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70, position[1] * 70, 70 - 1.5 * buff, 70 - 1.5 * buff))
                    pygame.display.update()
                    return

                if (sMat[x - 1][y - 1] != 0 and board[x - 1][
                    y - 1] == 0) and 0 < E.key - 48 < 10:  # pt estetica ca sa nu se suprapuna 2 valori
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70, position[1] * 70, 70 - 1.5 * buff, 70 - 1.5 * buff))
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70 + buff, position[1] * 70 + buff, 70 - 2 * buff, 70 - 2 * buff))
                    value = myFont.render(str(E.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0] * 70 + 8, position[1] * 70 - 12))
                    sMat[x - 1][y - 1] = E.key - 48
                    pygame.display.update()
                    return

                if 0 < E.key - 48 < 10:  # verific daca apas tastele 1-9 pentru a introduce valori in sMat
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70 + buff, position[1] * 70 + buff, 70 - 2 * buff, 70 - 2 * buff))
                    value = myFont.render(str(E.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0] * 70 + 8, position[1] * 70 - 12))
                    sMat[x - 1][y - 1] = E.key - 48
                    pygame.display.update()
                    return

                return


board = import_board_sudoku("Difficulty//easy.json")
sMat = [[board[j][i] for i in range(len(board[0]))] for j in range(len(board))]


def draw_table(win, font):
    for i in range(0, 9):
        for j in range(0, 9):
            if 0 < sMat[i][j] < 10:
                value = font.render(str(sMat[i][j]), True, element_color)
                win.blit(value, ((j + 1) * 70 + 8, (i + 1) * 70 - 12))
    pygame.display.update()


def Computer():
    global first, cromozomi, population, use_nsga
    if first:
        cromozomi = evolutive.generateCromozoms(board)
        cromozomi = sorted(cromozomi, key=lambda cromozom: evolutive.fitness(cromozom, board), reverse=True)
        best = cromozomi[0]
        first = False
    else:
        if use_nsga:
            cromozomi, vector = NSGA2.NSGA2(cromozomi, board)
            best = cromozomi[vector[0][random.randint(0, len(vector[0]) - 1)]]
        else:
            cromozomi = evolutive.EVOLUTIVE(cromozomi, board)
            best = cromozomi[0]
    return best


def updateTable(win, sMat):
    myFont = pygame.font.SysFont('Comic Sans MS', 45)
    for i in range(0, 9):
        for j in range(0, 9):
            position = (i + 1, j + 1)
            x, y = position[1], position[0]

            if board[x - 1][y - 1] == 0:
                if sMat[x - 1][y - 1] == 0:  # verific valoarea daca se apasa tasta 0 pentru a sterge valaorea din sMat
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70, position[1] * 70, 70 - 1.5 * buff, 70 - 1.5 * buff))

                elif (sMat[x - 1][y - 1] != 0 and board[x - 1][y - 1] == 0) and 0 < sMat[x - 1][y - 1] < 10:
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70, position[1] * 70, 70 - 1.5 * buff, 70 - 1.5 * buff))
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70 + buff, position[1] * 70 + buff, 70 - 2 * buff, 70 - 2 * buff))
                    value = myFont.render(str(sMat[x - 1][y - 1]), True, (0, 0, 0))
                    win.blit(value, (position[0] * 70 + 8, position[1] * 70 - 12))
                elif 0 < sMat[x - 1][y - 1] < 10:  # verific daca apas tastele 1-9 pentru a introduce valori in sMat
                    pygame.draw.rect(win, background_color,
                                     (position[0] * 70 + buff, position[1] * 70 + buff, 70 - 2 * buff, 70 - 2 * buff))
                    value = myFont.render(str(sMat[x - 1][y - 1]), True, (0, 0, 0))
                    win.blit(value, (position[0] * 70 + 8, position[1] * 70 - 12))


if __name__ == "__main__":

    # init table
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(background_color)
    myFont = pygame.font.SysFont('Comic Sans MS', 45)
    pygame.display.set_caption("Sudoku")

    # draw lines
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(window, (155, 0, 70), (55 + 70 * i, 55), (55 + 70 * i, 685), 6)
            pygame.draw.line(window, (155, 0, 70), (55, 55 + i * 70), (685, 55 + i * 70), 6)
        else:
            pygame.draw.line(window, (0, 0, 0), (55 + 70 * i, 58), (55 + 70 * i, 682), 3)
            pygame.draw.line(window, (0, 0, 0), (58, 55 + i * 70), (682, 55 + i * 70), 3)
    draw_table(window, myFont)
    while True:
        if winGame(sMat):
            time.sleep(5)
            print("\nFelicitari ai castigat jocul!\n")
            np.savetxt("Solved//rezolvare.txt", sMat, fmt="%d")
            break
        if player:
            for E in pygame.event.get():
                if E.type == pygame.MOUSEBUTTONUP and E.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 55 < pos[0] < 685 and 55 < pos[1] < 685:
                        insertValue(window, (pos[0] // 70, pos[1] // 70))
                if E.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        else:
            sMat = Computer()
            updateTable(window, sMat)
            pygame.display.update()
    for i in range(0, 9):
        for j in range(0, 9):
            print(sMat[i][j], end=" ")
        print("\n")