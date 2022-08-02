import random

def find_neighbors(board, row, col):
    """
    Get neighbors of a cell
    """
    neighbors = []
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i > -1 and j > -1 and j < len(board[0]) and i < len(board):
                neighbors.append((i, j))
                    
    return neighbors

def make_mines(board, size, mines_n, excep):
    """
    Place random mines on the board
    """
    avail = [(i, j) for i in range(size) for j in range(size)]
    avail.remove(excep)
    for i in range(mines_n):
        # Random row and column
        pos = random.choice(avail)
        row = pos[0]
        column = pos[1]
        avail.remove(pos)
        # print("Mine at ", row, column)
        # The random cell is not a mine
        if board[row][column] != "*":
            board[row][column] = "*"
            # Get all neighbors of the mine, and increment them
            neighbors = find_neighbors(board, row, column)
            for neighbor in neighbors:
                if board[neighbor[0]][neighbor[1]] != "*":
                    board[neighbor[0]][neighbor[1]] += 1
    # Return the resulted board
    return board