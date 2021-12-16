import sys
from board import Board
from player import playerFactory
from memento import Memento

import tkinter as tk
from tkinter import messagebox

class SantoriniGUI():
    """Display board and options"""

    def __init__(self, arg1, arg2, arg3, arg4):
        self._window = tk.Tk()
        self._window.title("Santorini")
        self._window.geometry("5000x5000")
        
        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=0, column=1, columnspan=5) # frame for 5x5 board grid
        self._turn_frame = tk.Frame(self._window)
        self._turn_frame.grid(row=1, column=1, columnspan=2) # frame for turn and player
        self._undo_frame = tk.Frame(self._window)
        self._undo_frame.grid(row=2, column=1, columnspan=3) # frame for optional undo/redo/next buttons
        self._score_frame = tk.Frame(self._window)
        self._score_frame.grid(row=3, column=1, columnspan=3) # frame for optional score display

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

        # TODO: implement grid buttons for clicking and add workers

        self._window.mainloop()
    
    # def run(self, caretaker):
    #     while True:
    #         # display
    #         self.board.display()

    #         # print turn and player
    #         if self._turn % 2 == 1:
    #             playerLabel = "white (AB)"
    #         else:
    #             playerLabel = "blue (YZ)"

    #         print("Turn: {0}, {1}".format(self._turn, playerLabel), end = '')

    #         # print score, note that this only occurs if currPlayer is heuristic
    #         if self._score:
    #             (move_score, height_score, center_score, distance_score) = self._currPlayer._move_score()
    #             print(", ({0}, {1}, {2})".format(height_score, center_score, distance_score))
    #         else:
    #             print("")

    #         # check if game ended
    #         if self.board.game_ended():
    #             sys.exit(0)

    #         # undo, redo, or next
    #         if self._redo:
    #             undo_redo = input("undo, redo, or next\n")
    #             if undo_redo == "undo":
    #                 # undo
    #                 caretaker.undo()
    #                 continue
    #             elif undo_redo == "redo":
    #                 # redo
    #                 caretaker.redo()
    #                 continue
    #             elif undo_redo == "next":
    #                 caretaker.wipe()
    #                 caretaker.incrementPointer()

    #         # move
    #         move = self._currPlayer.choose_move()
    #         self._turn += 1
    #         move.execute()

    #         # save the board after every move
    #         caretaker.backup()

    #         # switch players
    #         if self._turn % 2 == 0:
    #             self._currPlayer = self.board.player2
    #             self._otherPlayer = self.board.player1
    #         else:
    #             self._currPlayer = self.board.player1
    #             self._otherPlayer = self.board.player2

    # def save(self):
    #     """
    #     Saves the current state inside a memento.
    #     """
    #     board = self.board.copy()
    #     state = (board, self._turn)
    #     return Memento(state)

    # def restore(self, memento):
    #     """
    #     Restores the Originator's state from a memento object.
    #     """
    #     (self.board, self._turn) = memento.get_state()
    #     self._currPlayer = self.board.player1
    #     self._otherPlayer = self.board.player2