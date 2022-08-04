from tkinter import Button
from typing import TYPE_CHECKING
from time import time

from .utils import make_mines, find_neighbors

if TYPE_CHECKING:
    from .graphical_based import Tkinter


class Cell(Button):
    """Represents a cell in the board.

    :param game: The game instance.
    :param row: The row of the cell.
    :param column: The column of the cell.
    """

    def __init__(self, game: "Tkinter", row: int, column: int):
        super().__init__(game.root, image=game.unknown, command=self.mine, width=37.5, height=37.5)

        self.game = game
        self.row = row
        self.col = column
        self.bind("<Button-3>", self.flag)

    def mine(self):
        """Mines the cell."""
        if not self.game.started:
            self.game.started = True
            self.game.timer = time()
            self.game.actual_board = make_mines(
                self.game.actual_board,
                self.game.size,
                self.game.mines_n,
                (self.row, self.col),
                debug=False
            )
        if self.game.gameOver:
            return
        if not self.game.visual_board[self.row][self.col] == "M":
            if self.game.actual_board[self.row][self.col] == "*":
                self.game.game_over(False, self.row, self.col)
            else:
                self.game.visual_board[self.row][self.col] = "M"
                self.configure(
                    image=self.game.numbers[self.game.actual_board[self.row][self.col] - 1]
                    if self.game.actual_board[self.row][self.col] > 0
                    else self.game.mined
                )
                self.AMine(self.row, self.col)
                

    def AMine(self, row, column):
        """
        Automatic Click (Not repeated)

        :param row: The row of the cell.
        :param column: The column of the cell.

        :return: None
        """
        if (self.game.size * self.game.size) / 2 < self.game.mines_n: 
            return
        self.checked = set()
        self._AMine(row, column)
        

    def _AMine(self, row, column):
        """
        Automatic Click (Repeated)

        :param row: The row of the cell.
        :param column: The column of the cell.

        :return: None
        """
        if (row, column) in self.checked:
            return
        if self.game.visual_board[row][column] == "M" and len(self.checked) != 0:
            return
        self.checked.add((row, column))
        self.game.visual_board[row][column] = "M"
        self.game.cells[row][column].configure(image=self.game.numbers[self.game.actual_board[row][column] - 1]
                       if self.game.actual_board[row][column] > 0
                       else self.game.mined,
                       borderwidth=0,
                       highlightthickness=0)
        self.game.total_mined += 1
        if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
            self.game.game_over(True, self.row, self.col)
            return
        if self.game.actual_board[row][column] > 0:
            return
        else:
            for (i, j) in find_neighbors(self.game.actual_board, row, column):
                self._AMine(i, j)
            

    def flag(self, event):
        """Flags the cell.

        :param event: The default event received from
                    the tk button click dispatch.
        """
        if self.game.gameOver:
            return
        if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
            self.game.game_over(True, self.row, self.col)
        vB = self.game.visual_board
        if vB[self.row][self.col] == "F":
            self.configure(image=self.game.unknown)
            self.game.visual_board[self.row][self.col] = "N"
            if self.game.actual_board[self.row][self.col] == "*":
                self.game.c_f -= 1
        else:
            if not vB[self.row][self.col] == "M":
                self.game.visual_board[self.row][self.col] = "F"
                self.configure(image=self.game.flagged)
                if self.game.actual_board[self.row][self.col] == "*":
                    self.game.c_f += 1
                if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
                    self.game.game_over(True, self.row, self.col)
