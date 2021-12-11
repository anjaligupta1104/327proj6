"""
Meili and Anjali Gupta
CPSC 327 Pset
Saturday, 3:30 pm
"""

import sys
from board import Board
from player import Human

class SantoriniCLI:
    """Display board and options"""

    def __init__(self):
        self._board = Board()
        self._player1 = Human()
        self._player2 = Human()
        self._currPlayer = self._player1
        self._turn = 1
    
    def run(self):
        while True:
            # display
            self._board.display()
            if self._turn % 2 == 1:
                playerLabel = "white (AB)"
            else:
                playerLabel = "blue (YZ)"

            print("Turn: {0}, {0}".format(self._turn, playerLabel))

            # move
            self._currPlayer.move()

            # check if game ended
            if self._board.game_ended():
                sys.exit(0)
            
            
            
        
