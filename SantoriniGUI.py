import sys
from board import Board
from player import playerFactory
from memento import Caretaker, Memento

import tkinter as tk
from tkinter import messagebox

class SantoriniGUI():
    """Display board and options"""

    def __init__(self, arg1, arg2, arg3, arg4, caretaker):
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

        self.board = Board()
        player1 = playerFactory.build_player(self.board, arg1, 1)
        player2 = playerFactory.build_player(self.board, arg2, 2)
        self.board.set_player(player1)
        self.board.set_player(player2)

        self._currPlayer = player1
        self._otherPlayer = player2
        self._turn = 1
        self._redo = True if arg3 == "on" else False
        self._score = True if arg4 == "on" else False

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

        self._display_board()

        ended = self.board.game_ended()
        if ended:
            if (ended == 1):
                winner = "White"
            if (ended == 2):
                winner = "Blue"
            messagebox.showinfo(message=f"{winner} has won!")
            sys.exit(0)

        self._window.mainloop()

    def _move(self, i, j, caretaker):
        # function called every time a buttton on 5x5 grid is clicked
        # move should only be called when currPlayer is human TODO: implement this check
        # TODO: highlight legal moves
        # show warning if not legal move and return
        # otherwise highlight legal builds
        
        move = self._currPlayer.choose_move()
        self._turn += 1
        move.execute()
        caretaker.backup()

        if self._turn % 2 == 0:
            self._currPlayer = self.board.player2
            self._otherPlayer = self.board.player1
        else:
            self._currPlayer = self.board.player1
            self._otherPlayer = self.board.player2

        self._display_board(caretaker)

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
                tk.Button(self._board_frame, height = 7, width = 7, command = self._move(i,j, caretaker), image = self._image(i, j)).grid(row=i,column=j)
    
        if self._score:
            (move_score, height_score, center_score, distance_score) = self._currPlayer._move_score()
            score_text = f"{height_score}, {center_score}, {distance_score}"

            tk.Label(self._score_frame, 
                    text=score_text).grid(row=1, column=1)

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

    def save(self):
        """
        Saves the current state inside a memento.
        """
        board = self.board.copy()
        state = (board, self._turn)
        return Memento(state)

    def restore(self, memento):
        """
        Restores the Originator's state from a memento object.
        """
        (self.board, self._turn) = memento.get_state()
        self._currPlayer = self.board.player1
        self._otherPlayer = self.board.player2