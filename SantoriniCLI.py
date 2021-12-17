import sys
from board import Board
from player import playerFactory
from memento import Memento
from SantoriniGUIundo import SantoriniGUI

class SantoriniCLI:
    """Display board and options"""

    def __init__(self, arg1, arg2, arg3, arg4):
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
    
    def run(self, caretaker):
        SantoriniGUI(caretaker)

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
            
            
        
