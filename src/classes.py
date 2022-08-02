from tkinter import Button
from typing import TYPE_CHECKING

from .utils import make_mines

if TYPE_CHECKING:
    from .graphical_based import Tkinter


class Cell(Button):
    """Represents a cell in the board.

    :param game: The game instance.
    :param row: The row of the cell.
    :param column: The column of the cell.
    """

    def __init__(self, game: Tkinter, row: int, column: int):
        super().__init__(self.game.root, image=game.unknown, command=self.mine)

        self.game = game
        self.row = row
        self.col = column
        self.bind("<Button-3>", self.flag)

    def mine(self):
        """Mines the cell."""
        if not self.game.started:
            self.game.started = True
            self.game.actualBoard = make_mines(
                self.game.actualBoard,
                self.game.size,
                self.game.mines_n,
                (self.row, self.col),
            )
        if self.game.gameOver:
            return
        if not self.game.visualBoard[self.row][self.col] == "M":
            if self.game.actualBoard[self.row][self.col] == "*":
                self.game.game_over(False, self.row, self.col)
            else:
                self.game.visualBoard[self.row][self.col] = "M"
                self.configure(
                    image=self.game.numbers[self.game.actualBoard[self.row][self.col] - 1]
                    if self.game.actualBoard[self.row][self.col] > 0
                    else self.game.mined
                )
                self.game.total_mined += 1
                if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
                    self.game.game_over(True, self.row, self.col)
                # self.obj.auto_mine(self)

    def flag(self, event):
        """Flags the cell.

        :param event: The default event received from
                    the tk button click dispatch.
        """
        if self.game.gameOver:
            return
        vB = self.game.visualBoard
        if vB[self.row][self.col] == "F":
            self.configure(image=self.game.unknown)
            self.game.visualBoard[self.row][self.col] = "N"
            if self.game.actualBoard[self.row][self.col] == "*":
                self.game.c_f -= 1
        else:
            self.game.visualBoard[self.row][self.col] = "F"
            self.configure(image=self.game.flagged)
            if self.game.actualBoard[self.row][self.col] == "*":
                self.game.c_f += 1
            if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
                self.game.game_over(True, self.row, self.col)
