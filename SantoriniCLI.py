"""
Meili and Anjali Gupta
CPSC 327 Pset
Saturday, 3:30 pm
"""

import sys
from board import Board
from player import playerFactory

class SantoriniCLI:
    """Display board and options"""

    def __init__(self, arg1, arg2, arg3, arg4):
        self._board = Board()
        self._player1 = playerFactory.build_player(arg1, 1)
        self._player2 = playerFactory.build_player(arg2, 2)
        self._currPlayer = self._player1
        self._otherPlayer = self._player2
        self._turn = 1

        if arg3 == "off":
            self._redo = False
        else:
            self._redo = True

        if arg4 == "off":
            self._score = False
        else:
            self._score = True
    
    def run(self, caretaker):
        while True:
            # display
            self._board.display()

            # print turn, player, and score
            if self._turn % 2 == 1:
                playerLabel = "white (AB)"
            else:
                playerLabel = "blue (YZ)"

            print("Turn: {0}, {0}".format(self._turn, playerLabel))
    
            if self._score:
                print(", ({0}, {0}, {0})".format(self._currPlayer.height_score, self._currPlayer.center_score, self._currPlayer.distance_score))

            print("\n")

            # undo, redo, or next
            if self._redo:
                # TODO: implement undo/redo functionality
                undo_redo = input("undo, redo, or next\n")
                if undo_redo == "undo":
                    # undo
                    caretaker.undo()
                    continue
                else if undo_redo == "redo":
                    # redo
                    caretaker.redo()
                    continue

            # move
            self._currPlayer.move()

            # save the board after every move
            caretaker.backup()

            # check if game ended
            if self._board.game_ended():
                sys.exit(0)

            # switch players
            if self._turn % 2 == 1:
                self._currPlayer = self._player2
                self._otherPlayer = self._player1
            else:
                self._currPlayer = self._player1
<<<<<<< HEAD

    def save(self) -> Memento:
        """
        Saves the current state inside a memento.
        """

        return Memento(self._state)

    def restore(self, memento: Memento) -> None:
        """
        Restores the Originator's state from a memento object.
        """
        # TODO: change restore function
        self._state = memento.get_state()
=======
                self._otherPlayer = self._player2
>>>>>>> 6fcbb1a0c83921967d6d3fdcc85e0443ced408e2
            
            
            
        
