# Definirea tabloului Sudoku
board = [
	[0,5,0,0,0,0,0,0,4],
	[9,0,0,4,3,0,0,0,0],
	[0,0,0,2,0,9,3,8,0],
	[0,9,0,0,7,0,4,5,0],
	[3,0,0,0,0,2,0,0,0],
	[8,7,0,0,0,0,0,1,3],
	[5,0,1,0,0,8,0,0,0],
	[7,0,9,3,1,0,5,6,8],
	[6,0,4,7,2,5,0,3,9]
]

# Funcția pentru a verifica dacă un număr poate fi plasat într-o anumită poziție
def is_valid(board, row, col, num):
    # Verifică dacă numărul există deja în rând
    for x in range(9):
        if board[row][x] == num:
            return False

    # Verifică dacă numărul există deja în coloană
    for x in range(9):
        if board[x][col] == num:
            return False

    # Verifică dacă numărul există deja în cutia curentă
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

# Funcția pentru a rezolva jocul Sudoku
def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True

# Rezolvarea jocului Sudoku
solve_sudoku(board)

for i in range (0,9):
    for j in range (0,9):
        print(board[i][j],end = " ")
    print("\n")