import sys
from board import Board
from player import playerFactory

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
        self._score = True if arg4 == "off" else False
    
    def run(self):
        while True:
            # display
            self.board.display()

            # print turn and player
            if self._turn % 2 == 1:
                playerLabel = "white (AB)"
            else:
                playerLabel = "blue (YZ)"

            print("Turn: {0}, {0}".format(self._turn, playerLabel))
    
            # print score, note that this only occurs if currPlayer is heuristic
            if self._score:
                print(", ({0}, {0}, {0})".format(self._currPlayer.height_score, self._currPlayer.center_score, self._currPlayer.distance_score))

            print("\n")

            # move
            move = self._currPlayer.choose_move()
            move.execute()

            # check if game ended
            if self._board.game_ended():
                sys.exit(0)

            # switch players
            if self._turn % 2 == 1:
                self._currPlayer = self.board.player2
                self._otherPlayer = self.board.player1
            else:
                self._currPlayer = self.board.player1
                self._otherPlayer = self.board.player2
            
            
            
        
