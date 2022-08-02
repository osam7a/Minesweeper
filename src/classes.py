from tkinter import Button
from typing import TYPE_CHECKING

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
        super().__init__(game.root, image=game.unknown, command=self.mine)

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
                # self.AMine(self.row, self.col)

    def AMine(self, row, column):
        self.checked = set((row, column))
        self._AMine(row, column)

    def _AMine(self, row, column):
        neighbors = find_neighbors(self.game.actualBoard, row, column, False)
        for neighbor in neighbors:
            if neighbor in self.checked:
                continue
            if not isinstance(self.game.actualBoard[neighbor[0]][neighbor[1]], str):
                self.checked.add(neighbor)
                self.game.visualBoard[neighbor[0]][neighbor[1]] = "M"
                self.game.total_mined += 1
                self.game.cells[neighbor[0]][neighbor[1]].configure(
                    image=self.game.mined if self.game.actualBoard[row][column] == 0 else self.game.numbers[self.game.actualBoard[row][column] - 1]
                )
                if not self.game.actualBoard[neighbor[0]][neighbor[1]] > 0:
                    self._AMine(neighbor[0], neighbor[1])

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
            if not vB[self.row][self.col] == "M":
                self.game.visualBoard[self.row][self.col] = "F"
                self.configure(image=self.game.flagged)
                if self.game.actualBoard[self.row][self.col] == "*":
                    self.game.c_f += 1
                if self.game.c_f + self.game.total_mined == self.game.size * self.game.size:
                    self.game.game_over(True, self.row, self.col)
