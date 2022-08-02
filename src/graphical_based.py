import json
from tkinter import Button, Menu, PhotoImage, Tk
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askinteger

from .classes import Cell


LOST_MESSAGE = lambda flags, bombs: f"""
You lost the game!
Defused Bombs: {flags}
Remaining Bombs: {bombs - flags}
"""
WIN_MESSAGE = lambda flags, bombs: f"""
You won the game!
Defused Bombs: {flags}
Remaining Bombs: {bombs - flags}
"""


def rest(root):
    root.destroy()
    main()


def changeSize(root, size, mine_count):
    root.destroy()
    load = json.load(open("config.json"))
    load["mines_n"] = mine_count
    load["size"] = size
    json.dump(load, open("config.json", "w"))
    main()


def customSize(root):
    size = askinteger(
        "Custom Size", "Enter the size of the board:", minvalue=2, maxvalue=18
    )
    mines = askinteger(
        "Mines", "Enter number of mines:", minvalue=1, maxvalue=size * size
    )
    changeSize(root, size, mines)


class Tkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")

        # Configuration
        self.conf = json.load(open("config.json"))
        self.mines_n = self.conf["mines_n"]
        self.size = self.conf["size"]
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
        self.actualBoard = [[0 for i in range(self.size)] for x in range(self.size)]
        self.visualBoard = [["N" for i in range(self.size)] for x in range(self.size)]

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
        self.root.mainloop()

    def game_over(self, win, row, col):
        cell = self.cells[row][col]
        if not win:
            cell.configure(image=self.exploded)
        self.gameOver = True
        for _row in self.cells:
            for _cell in _row:
                if self.actualBoard[_cell.row][_cell.col] == "*":
                    if not win:
                        if not _cell == cell:

                            if self.visualBoard[_cell.row][_cell.col] == "F":
                                _cell.configure(image=self.flag_correct)
                            else:
                                _cell.configure(image=self.bomb)
                    else:
                        if self.visualBoard[_cell.row][_cell.col] == "F":
                            _cell.configure(image=self.flag_correct)
                        else:
                            _cell.configure(image=self.bomb)
                elif self.visualBoard[_cell.row][_cell.col] == "F":
                    _cell.configure(image=self.flag_wrong)
        showinfo("Game Over", LOST_MESSAGE(self.c_f, self.mines_n) if not win else WIN_MESSAGE(self.c_f, self.mines_n))

    def load_board(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = Cell(self, i, j)
                btn.grid(row=i, column=j, sticky="nswe")
                self.cells[i][j] = btn


def main():
    Tkinter()
