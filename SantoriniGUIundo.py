# version of SantoriniGUI with SantoriniGUI inheriting from SantoriniCLI

import sys
from SantoriniCLI_noGUI import SantoriniCLI
from board import Board
from player import playerFactory
from memento import Caretaker, Memento
from tkinter.constants import ACTIVE, DISABLED

import tkinter as tk
from tkinter import messagebox

class SantoriniGUI(SantoriniCLI):
    """Display board and options"""

    def __init__(self, caretaker):
        self._window = tk.Tk()
        self._window.title("Santorini")
        self._window.geometry("550x800")
        self._window.config(bg="skyblue")

        # frame for 5x5 board grid
        self._board_frame = tk.Frame(self._window, width = 500, height = 500)
        self._board_frame.grid(row=0, column=0, columnspan=5, padx=25, pady=25)

        # frame for turn and player 
        self._turn_frame = tk.Frame(self._window)
        self._turn_frame.grid(row=1, column=1, columnspan=2)

        # frame for optional score display
        self._score_frame = tk.Frame(self._window)
        self._score_frame.grid(row=3, column=1) 

        # choose and execute move
        if (self._currPlayer.type == "human"):
            self._choose_worker()
        else:
            move = self._currPlayer.choose_move()
            move.execute()
        self._display_board()

        caretaker.backup()
        self._turn += 1
        if self._turn % 2 == 0:
            self._currPlayer = self.board.player2
            self._otherPlayer = self.board.player1
        else:
            self._currPlayer = self.board.player1
            self._otherPlayer = self.board.player2

        if self._redo:
            self._undo_frame = tk.Frame(self._window)
            self._undo_frame.grid(row=2, column=1, columnspan=3) # frame for optional undo/redo/next buttons

            tk.Button(self._undo_frame, 
                    text="Next", 
                    command=self._next_move(caretaker)).grid(row=1, column=1)
            tk.Button(self._undo_frame, 
                    text="Undo", 
                    command=self._undo_move(caretaker)).grid(row=1, column=2)
            tk.Button(self._undo_frame, 
                    text="Redo", 
                    command=self._redo_move(caretaker)).grid(row=1, column=2)

        ended = self.board.game_ended()
        if ended:
            if (ended == 1):
                winner = "White"
            if (ended == 2):
                winner = "Blue"
            messagebox.showinfo(message=f"{winner} has won!")
            sys.exit(0)

        self._window.mainloop()

    def _image(self, i, j):
        level = self.board.buildings[i][j]
        worker = self.board.workers[i][j]

        if (worker == 'Y' or worker == 'Z'):
            worker = "blue"
        elif (worker == 'A' or worker == 'B'):
            worker = "white"
        else:
            worker = ""

        img_name = f"{worker}level{level}.jpg"
        return img_name

    def _display_board(self, caretaker):
        for x in self._turn_frame.winfo_children():
            x.destroy()
        for x in self._score_frame.winfo_children():
            x.destroy()
        for x in self._board_frame.winfo_children():
            x.destroy()

        if self._turn % 2 == 1:
            playerLabel = "white (AB)"
        else:
            playerLabel = "blue (YZ)"

        turn_text = f"Turn: {self._turn}, {playerLabel}"
        tk.Label(self._turn_frame, 
                text=turn_text).grid(row=1, column=1, columnspan=2)

        for i in range(5):
            for j in range(5):
                tk.Button(self._board_frame, height = 7, width = 7, image = self._image(i, j)).grid(row=i,column=j)
    
        if self._score:
            (move_score, height_score, center_score, distance_score) = self._currPlayer._move_score()
            score_text = f"{height_score}, {center_score}, {distance_score}"

            tk.Label(self._score_frame, 
                    text=score_text).grid(row=1, column=1)

    def _legal_worker(self, piece_num):
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        for move_num in range(8):
            for build_num in range(8):
                move_dir = directions[move_num]
                build_dir = directions[build_num]
                self._currPlayer._set_temp(piece_num)

                if self._currPlayer._try_move(move_dir) and self._currPlayer._try_build(build_dir):
                    return True
        return False

    def _choose_worker(self):
        """Displays the board with only buttons with player's workers (with legal moves) on them enabled."""
        # initialize piece locations and board
        piece1 = self._currPlayer.piece1.location 
        piece2 = self._currPlayer.piece1.location
        buttons = [[None for col in range(5)] for row in range(5)]
        for i in range(5):
            for j in range(5):
                button = tk.Button(self._board_frame, height = 7, width = 7, command = self._choose_move(i,j), image = self._image(i,j), state = DISABLED, bg = "white")
                buttons[i][j] = button

        # enable buttons at piece locations if legal, end game if no legal pieces
        if self._legal_worker(1):
            buttons[piece1[0]][piece1[1]]["state"] = ACTIVE
            buttons[piece1[0]][piece1[1]]["bg"] = "red"
        elif self._legal_worker(2):
            buttons[piece2[0]][piece2[1]]["state"] = ACTIVE
            buttons[piece1[0]][piece1[1]]["bg"] = "red"
        else: # no legal moves, game ended
            winner = "White" if self._currPlayer.player_num == 1 else "Blue"
            messagebox.showinfo(message=f"{winner} has won!")
            sys.exit(0)

        # draw board
        for i in range(5):
            for j in range(5):
                buttons[i][j].grid(row=i,column=j)

    # copied from player.py
    def _get_dir(self, dir):
        directions = {
            "n": [-1,0],
            "ne": [-1,1],
            "e": [0,1],
            "se": [1,1],
            "s": [1,0],
            "sw": [1,-1],
            "w": [0,-1],
            "nw": [-1,-1]
        }
        return directions.get(dir)

    # copied from player.py with slight modifications
    def _legal_move(self, i, j, dir):
        move = self._get_dir(dir)
        new_x = i + move[0]
        new_y = j + move[1]
        in_bounds = new_x >= 0 and new_x <= 4 and new_y >= 0 and new_y <= 4

        if in_bounds:
            free = self.board.workers[new_x][new_y] == 0
            height_diff = self.board.buildings[new_x][new_y] - self.board.buildings[i][j] <= 1

            if free and height_diff:
                self._temp_workers[i][j] = 0
                self._temp_location = [new_x, new_y]
                return True
            else:
                return False
        else:
            return False

    def _choose_move(self, piece_x, piece_y):
        """Displays the board with only valid moves from i,j enabled."""
        # initialize board
        buttons = [[None for col in range(5)] for row in range(5)]
        for i in range(5):
            for j in range(5):
                button = tk.Button(self._board_frame, height = 7, width = 7, command = self._choose_build(piece_x, piece_y, i,j), image = self._image(), state = DISABLED, bg = "white")
                buttons[i][j] = button

        # enable buttons that represent legal moves
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        for move_num in range(8):
            if self._legal_move(i,j,directions[move_num]):
                move = self._get_dir(dir)
                move_x = i + move[0]
                move_y = j + move[1]
                buttons[move_x][move_y]["state"] = ACTIVE
                buttons[move_x][move_y]["bg"] = "orange"

        # redraw board
        for i in range(5):
            for j in range(5):
                buttons[i][j].grid(row=i,column=j)

    def _build(self,i,j):
        self.board.buildings[i][j] += 1

    # copied from player.py with slight modifications
    def _legal_build(self, i, j, dir):
        build = self._get_dir(dir)
        build_x = i + build[0]
        build_y = j + build[1]
        in_bounds = build_x >= 0 and build_x <= 4 and build_y >= 0 and build_y <= 4

        if in_bounds:
            height_4 = self.board.buildings[build_x][build_y] < 4
            free = self._temp_workers[build_x][build_y] == 0

            return height_4 and free
        else:
            return False

    def _choose_build(self, piece_x, piece_y, new_x, new_y):
        """Displays the board with only valid builds from i,j enabled."""
        # update piece location
        piece = self._currPlayer.piece1 if self.board.workers[piece_x, piece_y] in {'A', 'Y'} else self._currPlayer.piece2
        piece.location = [new_x,new_y]
        # update workers
        self.board.workers[piece_x][piece_y] = 0
        self.board.workers[new_x][new_y] = piece.name 

        # initialize board
        buttons = [[None for col in range(5)] for row in range(5)]
        for i in range(5):
            for j in range(5):
                button = tk.Button(self._board_frame, height = 7, width = 7, command = self._build(i,j), image = self._image(), state = DISABLED, bg = "white")
                buttons[i][j] = button

        # enable buttons that represent legal moves
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        for move_num in range(8):
            if self._legal_move(i,j,directions[move_num]):
                move = self._get_dir(dir)
                move_x = i + move[0]
                move_y = j + move[1]
                buttons[move_x][move_y]["state"] = ACTIVE
                buttons[move_x][move_y]["bg"] = "orange"

        # redraw board
        for i in range(5):
            for j in range(5):
                buttons[i][j].grid(row=i,column=j)

    def _display_board(self):
        """Displays the board at end of each turn."""
        for i in range(5):
            for j in range(5):
                button = tk.Button(self._board_frame, height = 7, width = 7, image = self._image())
                button.grid(row=i,column=j)

    def _next_move(self, caretaker):
        caretaker.wipe()
        caretaker.incrementPointer()
        self._display_board(caretaker)

    def _undo_move(self, caretaker):
        caretaker.undo()
        self._display_board(caretaker)

    def _redo_move(self, caretaker):
        caretaker.redo()
        self._display_board(caretaker)