import json
from tkinter import Button, Menu, PhotoImage, Tk
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askinteger
from time import time

from .classes import Cell

LOST_MESSAGE = lambda flags, bombs, finish: f"""
You lost the game!
Defused Bombs: {flags}
Remaining Bombs: {bombs - flags}
Time: {finish} seconds
"""
WIN_MESSAGE = lambda flags, bombs, finish: f"""
You won the game!
Defused Bombs: {flags}
Remaining Bombs: {bombs - flags}
High Score: {get_config("high_score")} seconds
{"New High Score!" if get_config("high_score") < finish else ""}
"""
HOW_TO_PLAY = """
What is minesweeper?
Minesweeper is a puzzle game, in which the player tries to clear a rectangular board of cells by flagging every mine around the board and by clearing every cell without a mine

How to play minesweeper?
Every cell around a mine has a number, this number indicates how many mines are around this cell, if there is 2 mines the number is 2, if there is 3 mines the number is 3, if there is no mines there is no number and so on.

What are the controls?
To start the game, click anywhere on the board.
To flag a cell, click on it with the right mouse button.
To clear a cell, click on it with the left mouse button.
"""


def rest(root):
    """
    Restarts the game.

    :param root: The window root of the game.

    :return: None
    """
    root.destroy()
    main(False)


def showHelp():
    """
    Shows the help dialog.

    :return: None
    """
    showinfo("How to play", HOW_TO_PLAY)
    showinfo("Note", "First click will always be clear, and has no number! (Unless you're playing with a board that's under 4x4)")


def get_config(k):
    """
    Gets the configuration from the config.json file.

    :return: The configuration.
    """
    return json.load(open("config.json"))[k]

def set_config(k, v):
    """
    Sets the configuration in the config.json file.

    :param k: The key of the configuration.
    :param v: The value of the configuration.

    :return: None
    """
    load = json.load(open("config.json"))
    load[k] = v
    json.dump(load, open("config.json", "w"))


def changeSize(root, size, mine_count):
    """
    Changes the size of the board.

    :param root: The window root of the game.
    :param size: The size of the new board.
    :param mine_count: The number of mines in the new board.

    :return: None
    """
    root.destroy()
    set_config("mines_n", mine_count)
    set_config("size", size)
    main(False)


def customSize(root):
    """
    Makes dialogs to change the size of the board.

    :param root: The window root of the game.

    :return: None
    """
    size = askinteger(
        "Custom Size", "Enter the size of the board:", minvalue=2, maxvalue=18
    )
    mines = askinteger(
        "Mines", "Enter number of mines:", minvalue=1, maxvalue=size * size
    )
    changeSize(root, size, mines)


class Tkinter:
    def __init__(self, first_game):
        self.root = Tk()
        self.root.title("Minesweeper")

        # Configuration
        self.conf = json.load(open("config.json"))
        self.mines_n = get_config("mines_n")
        self.size = get_config("size")
        self.mines_left = self.mines_n
        self.gameOver = False
        self.c_f = 0
        self.total_mined = 0
        self.started = False

        # Images
        self.flagged = PhotoImage(file="images/TileFlag.png")
        self.flagged = self.flagged.subsample(5, 5)
        self.bomb = PhotoImage(file="images/TileMine.png")
        self.bomb = self.bomb.subsample(5, 5)
        self.mined = PhotoImage(file="images/TileEmpty.png")
        self.mined = self.mined.subsample(5, 5)
        self.unknown = PhotoImage(file="images/TileUnknown.png")
        self.unknown = self.unknown.subsample(5, 5)
        self.exploded = PhotoImage(file="images/TileExploded.png")
        self.exploded = self.exploded.subsample(5, 5)
        self.flag_correct = PhotoImage(file="images/TileFlagCorrect.png")
        self.flag_correct = self.flag_correct.subsample(5, 5)
        self.flag_wrong = PhotoImage(file="images/TileFlagInCorrect.png")
        self.flag_wrong = self.flag_wrong.subsample(5, 5)
        self.numbers = [
            PhotoImage(file="images/Tile1.png").subsample(5, 5),
            PhotoImage(file="images/Tile2.png").subsample(5, 5),
            PhotoImage(file="images/Tile3.png").subsample(5, 5),
            PhotoImage(file="images/Tile4.png").subsample(5, 5),
            PhotoImage(file="images/Tile5.png").subsample(5, 5),
            PhotoImage(file="images/Tile6.png").subsample(5, 5),
            PhotoImage(file="images/Tile7.png").subsample(5, 5),
            PhotoImage(file="images/Tile8.png").subsample(5, 5),
        ]
        self.visited = []

        # Arrays
        self.cells = [[i for i in range(self.size)] for x in range(self.size)]
        self.actual_board = [[0 for i in range(self.size)] for x in range(self.size)]
        self.visual_board = [["N" for i in range(self.size)] for x in range(self.size)]

        Button(self.root, text="Restart", command=lambda: rest(self.root)).grid(
            row=self.size + 1, column=0, columnspan=self.size, sticky="nswe"
        )
        menu = Menu(self.root)
        self.root.config(menu=menu)
        settings = Menu(menu)
        settings.add_command(
            label="8x8 Size (10 Mines)", command=lambda: changeSize(self.root, 8, 10)
        )
        settings.add_command(
            label="12x12 Size (60 Mines)", command=lambda: changeSize(self.root, 12, 60)
        )
        settings.add_command(
            label="18x18 Size (120 Mines)", command=lambda: changeSize(self.root, 18, 120)
        )
        settings.add_command(label="Custom", command=lambda: customSize(self.root))
        menu.add_cascade(label="Settings", menu=settings)
        exitg = Menu(menu)
        exitg.add_command(label="Exit", command=lambda: self.root.destroy())
        menu.add_cascade(label="Exit", menu=exitg)

        self.load_board()
        if first_game:
            showHelp()
            first_game = True
        self.timer = None
        self.root.mainloop()

    def game_over(self, win, row, col):
        """
        Game Over

        :param win: Whether the player won or not
        :param row: Row of the losing cell
        :param col: Column of the losing cell

        :return: None
        """

        cell = self.cells[row][col]
        if not win:
            cell.configure(image=self.exploded)
        self.gameOver = True
        for _row in self.cells:
            for _cell in _row:
                if self.actual_board[_cell.row][_cell.col] == "*":
                    if not win:
                        if not _cell == cell:

                            if self.visual_board[_cell.row][_cell.col] == "F":
                                _cell.configure(image=self.flag_correct)
                            else:
                                _cell.configure(image=self.bomb)
                    else:
                        if self.visual_board[_cell.row][_cell.col] == "F":
                            _cell.configure(image=self.flag_correct)
                        else:
                            _cell.configure(image=self.bomb)
                elif self.visual_board[_cell.row][_cell.col] == "F":
                    _cell.configure(image=self.flag_wrong)
        end_time = time()
        finish = end_time - self.timer
        finish = round(finish, 2)
        if finish < get_config("high_score") and win:
            set_config("high_score", finish)
        showinfo("Game Over", LOST_MESSAGE(self.c_f, self.mines_n, finish) if not win else WIN_MESSAGE(self.c_f, self.mines_n, finish))

    def load_board(self):
        """
        Loads the board

        :return: None
        """
        for i in range(self.size):
            for j in range(self.size):
                btn = Cell(self, i, j)
                btn.grid(row=i, column=j, sticky="nswe")
                self.cells[i][j] = btn



def main(first_game):
    return Tkinter(first_game)
    
