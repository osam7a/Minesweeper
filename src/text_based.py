

# -----------------------------------------------
#               By Osama Alhennawi
# -----------------------------------------------


from colorama import Fore

from utils import make_mines

mines_n = 8
size = 8

# Make the boards as 2D Arrays
actualBoard = [[0 for i in range(size)] for x in range(size)]
visualBoard = [["N" for i in range(size)] for x in range(size)]


def render(b):
    """Render the gameplay board.

    Visually renders the board.

    :param board: The board to render.
    """
    print("     1       2       3       4       5       6       7       8")
    print("  _______________________________________________________________")
    for _i, i in enumerate(b):
        # Print row number
        print(_i + 1, end=" ")
        for _j, j in enumerate(i):
            # Print cell
            print("│ ", j, " │", end=" ")
        # New line
        print()
    print("  _______________________________________________________________")


# Place mines
print("Hello, welcome to this minesweeper game!, use the following format to play: <flag or mine> <row>, <column>")
mines_str = int(input("Total mines: "))
mines_n = mines_str
print("Making board...")
actualBoard = make_mines(actualBoard, size)
print("Board made!")
points = 0
while True:
    # First render
    render(visualBoard)
    inp = input("INPUT: ")
    # Format input
    f_m = inp[:4]
    r_c = inp[4:].strip().split(",")
    row = int(r_c[0]) - 1
    column = int(r_c[1]) - 1
    if f_m == "flag":
        # Flag cell
        visualBoard[row][column] = "F"
        if actualBoard[row][column] == "*":
            points += 1
        render(visualBoard)
    else:
        if actualBoard[row][column] == "*":
            # Player lost
            visualBoard[row][column] = f"{Fore.RED}*{Fore.RESET}"
            for _i, r in enumerate(visualBoard):
                for _j, col in enumerate(r):
                    if col == "F":
                        if actualBoard[_i][_j] == "*":
                            visualBoard[_i][_j] = f"{Fore.GREEN}*{Fore.RESET}"
                        else:
                            visualBoard[_i][_j] = f"{Fore.RED}F{Fore.RESET}"
                    else:
                        if actualBoard[_i][_j] == "*":
                            visualBoard[_i][_j] = f"{Fore.RED}*{Fore.RESET}"

            render(visualBoard)
            print("GAME OVER!")
            print("Total correct flagged mines: ", points)
            break
        else:
            visualBoard[row][column] = actualBoard[row][column]
            render(visualBoard)
