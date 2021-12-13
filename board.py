"""
Meili and Anjali Gupta
CPSC 327 Pset
Saturday, 3:30 pm
"""

class Board:

    def __init__(self):
        self.buildings = [[0 for col in range(5)] for row in range(5)]
        self._workers = [[0 for col in range(5)] for row in range(5)]
        self._workers[1][1] = 'Y'
        self._workers[1][3] = 'B'
        self._workers[3][1] = 'A'
        self._workers[3][3] = 'Z'

    def display(self):
        for i in range(5):
            print("+--+--+--+--+--+\n")
            for j in range(5):
                print("|")
                print(self._buildings[i][j])
                if self._workers[i][j] != 0:
                    print(self._workers[i][j])
                else:
                    print(" ")
            print("|\n")

    def game_ended(self):
        for i in range(5):
            for j in range(5):
                if self._buildings[i][j] == 3 and self._workers[i][j] != 0:
                    if self._workers[i][j] == 'A' or self._workers[i][j] == 'B':
                        playerLabel = "white"
                    else:
                        playerLabel = "blue"

                    print(playerLabel + "has won")
                    return True

        return False