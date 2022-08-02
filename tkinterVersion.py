

# -----------------------------------------------
#               By Osama Alhennawi
#             Assests from https://github.com/zigurous/unity-minesweeper-tutorial/tree/main/Assets/Sprites
# -----------------------------------------------


# Imports
import random
import json
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *



class Cell(Button):
    def __init__(self, tk, row, column):
        self.obj = tk
        self.row = row
        self.col = column
        super().__init__(self.obj.root, image=tk.unknown, command = self.mine)
        self.bind("<Button-3>", self.flag)
    
    def mine(self):
        if not self.obj.started == True:
            self.obj.started = True
            self.obj.actualBoard = self.obj.make_mines(self.obj.actualBoard, self.obj.size, self.obj.mines_n, (self.row, self.col))
        if self.obj.gameOver:
            return
        if not self.obj.visualBoard[self.row][self.col] == "M":
            if self.obj.actualBoard[self.row][self.col] == "*":
                self.obj.game_over(False, self.row, self.col)
            else:
                self.obj.visualBoard[self.row][self.col] = "M"
                self.configure(image=self.obj.numbers[self.obj.actualBoard[self.row][self.col]-1] if self.obj.actualBoard[self.row][self.col] > 0 else self.obj.mined)
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
    size = askinteger("Custom Size", "Enter the size of the board:", minvalue=2, maxvalue=18)
    mines = askinteger("Mines", "Enter number of mines:", minvalue=1, maxvalue=size * size-4)
    changeSize(root, size, mines)

class Tkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")

        # Configuration
        self.conf = json.load(open('config.json'))
        self.mines_n = self.conf['mines_n']
        self.size = self.conf['size']
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
        self.numbers = [PhotoImage(file="images/Tile1.png").subsample(5, 5), PhotoImage(file="images/Tile2.png").subsample(5, 5), PhotoImage(file="images/Tile3.png").subsample(5, 5), PhotoImage(file="images/Tile4.png").subsample(5, 5), PhotoImage(file="images/Tile5.png").subsample(5, 5), PhotoImage(file="images/Tile6.png").subsample(5, 5), PhotoImage(file="images/Tile7.png").subsample(5, 5), PhotoImage(file="images/Tile8.png").subsample(5, 5)]
        self.visited = []

        # Arrays
        self.cells = [[i for i in range(self.size)] for x in range(self.size)]
        self.actualBoard = [[0 for i in range(self.size)] for x in range(self.size)]
        self.visualBoard = [["N" for i in range(self.size)] for x in range(self.size)]

        Button(self.root, text="Restart", command=lambda: rest(self.root)).grid(row=self.size+1, column=0, columnspan=self.size, sticky=N+W+S+E)
        menu = Menu(self.root)
        self.root.config(menu=menu)
        settings = Menu(menu)
        settings.add_command(label="8x8 Size (10 Mines)", command=lambda: changeSize(self.root, 8, 10))
        settings.add_command(label="12x12 Size (60 Mines)", command=lambda: changeSize(self.root, 12, 60))
        settings.add_command(label="18x18 Size (120 Mines)", command=lambda: changeSize(self.root, 18, 120))
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
                if _cell.obj.actualBoard[_cell.row][_cell.col] == "*":
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
        showinfo("Game Over", "You lost!" if not win else "You win!")

    # def auto_mine(self, cell):
    #     neighbors = self.find_neighbors(self.actualBoard, cell.row, cell.col)
    #     neighbors = filter(lambda i: i not in self.visited, neighbors)
    #     for neighbor in neighbors:
    #         _neighbor = self.actualBoard[neighbor[0]][neighbor[1]]
    #         self.visited.append(neighbor)
    #         _cell = self.cells[neighbor[0]][neighbor[1]]
    #         if _neighbor != "*":
    #             _cell.configure(image=self.mined)
    #             self.auto_mine(_cell)

    def make_mines(self, board, size, mines_n, excep):
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
                neighbors = self.find_neighbors(board, row, column)
                for neighbor in neighbors:
                    if board[neighbor[0]][neighbor[1]] != "*":
                        board[neighbor[0]][neighbor[1]] += 1
        # Return the resulted board
        return board

    def load_board(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = Cell(self, i, j)
                btn.grid(row=i, column=j, sticky=N+W+S+E)
                self.cells[i][j] = btn

    def find_neighbors(self, board, row, col):
        """
        Get neighbors of a cell
        """
        neighbors = []
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i > -1 and j > -1 and j < len(board[0]) and i < len(board):
                    neighbors.append((i, j))
                    
        return neighbors

def main():
    tk = Tkinter()

if __name__ == "__main__":
    main()