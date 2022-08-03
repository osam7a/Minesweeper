import random


def find_neighbors(board, row, col, diagonal=True):
    """Finds the neighbors of a cell.

    :param board: The board to search.
    :param row: The row of the cell.
    :param col: The column of the cell.
    :param diagonal: Whether to include diagonal neighbors or not.

    :return: A list of neighbouring cells.
    """
    neighbors = []
    if diagonal:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i > -1 and j > -1 and j < len(board[0]) and i < len(board):
                    neighbors.append((i, j))
    else:
        if row - 1 >= 0:
            neighbors.append((row - 1, col))
        if row + 1 < len(board):
            neighbors.append((row + 1, col))
        if col - 1 >= 0:
            neighbors.append((row, col - 1))
        if col + 1 < len(board[0]):
            neighbors.append((row, col + 1))

    return neighbors


def make_mines(board, size, mines_n=8, excep=None):
    """Place random mines on the board

    :param board: The board to make the mines on.
    :param size: The size of the board.
    :param mines_n: The number of mines to create.
    :excep: The cell to exclude from the mines.

    :return: The created board.
    """
    avail = [(i, j) for i in range(size) for j in range(size)]
    if excep:
        if not size < 9:
            avail.remove(excep)
            avail.remove((excep[0]-1, excep[1]))
            avail.remove((excep[0]+1, excep[1]))
            avail.remove((excep[0], excep[1]-1))
            avail.remove((excep[0], excep[1]+1))
            avail.remove((excep[0]-1, excep[1]-1))
            avail.remove((excep[0]-1, excep[1]+1))
            avail.remove((excep[0]+1, excep[1]-1))
            avail.remove((excep[0]+1, excep[1]+1))


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
