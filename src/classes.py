from tkinter import Button
from .utils import make_mines


class Cell(Button):
    def __init__(self, tk, row, column):
        self.obj = tk
        self.row = row
        self.col = column
        super().__init__(self.obj.root, image=tk.unknown, command=self.mine)
        self.bind("<Button-3>", self.flag)

    def mine(self):
        if not self.obj.started:
            self.obj.started = True
            self.obj.actualBoard = make_mines(
                self.obj.actualBoard,
                self.obj.size,
                self.obj.mines_n,
                (self.row, self.col),
            )
        if self.obj.gameOver:
            return
        if not self.obj.visualBoard[self.row][self.col] == "M":
            if self.obj.actualBoard[self.row][self.col] == "*":
                self.obj.game_over(False, self.row, self.col)
            else:
                self.obj.visualBoard[self.row][self.col] = "M"
                self.configure(
                    image=self.obj.numbers[self.obj.actualBoard[self.row][self.col] - 1]
                    if self.obj.actualBoard[self.row][self.col] > 0
                    else self.obj.mined
                )
                self.obj.total_mined += 1
                if self.obj.c_f + self.obj.total_mined == self.obj.size * self.obj.size:
                    self.obj.game_over(True, self.row, self.col)
                # self.obj.auto_mine(self)

    def flag(self, event):
        if self.obj.gameOver:
            return
        vB = self.obj.visualBoard
        if vB[self.row][self.col] == "F":
            self.configure(image=self.obj.unknown)
            self.obj.visualBoard[self.row][self.col] = "N"
            if self.obj.actualBoard[self.row][self.col] == "*":
                self.obj.c_f -= 1
        else:
            self.obj.visualBoard[self.row][self.col] = "F"
            self.configure(image=self.obj.flagged)
            if self.obj.actualBoard[self.row][self.col] == "*":
                self.obj.c_f += 1
            if self.obj.c_f + self.obj.total_mined == self.obj.size * self.obj.size:
                self.obj.game_over(True, self.row, self.col)
