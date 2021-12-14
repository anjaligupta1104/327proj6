class Board:

    def __init__(self):
        # initialize board
        self.buildings = [[0 for col in range(5)] for row in range(5)]
        self.workers = [[0 for col in range(5)] for row in range(5)]

        # initialize workers
        self.workers[1][1] = 'Y'
        self.workers[1][3] = 'B'
        self.workers[3][1] = 'A'
        self.workers[3][3] = 'Z'

        # initialize players
        self.player1 = None
        self.player2 = None

    def set_player(self, player):
        if player.player_num == 1:
            self.player1 = player
        else:
            self.player2 = player

    def display(self):
        for i in range(5):
            print("+--+--+--+--+--+")
            for j in range(5):
                print("|", end = '')
                print(self.buildings[i][j], end = '')
                if self.workers[i][j] != 0:
                    print(self.workers[i][j], end = '')
                else:
                    print(" ", end = '')
            print("|")
        print("+--+--+--+--+--+")

    def game_ended(self):
        moves = self.player1._enumerate_valid_moves()
        if not moves:
            print("blue has won")
            return True

        moves = self.player2._enumerate_valid_moves()
        if not moves:
            print("white has won")
            return True

        for i in range(5):
            for j in range(5):
                if self.buildings[i][j] == 3 and self.workers[i][j] != 0:
                    if self.workers[i][j] == 'A' or self.workers[i][j] == 'B':
                        playerLabel = "white"
                    else:
                        playerLabel = "blue"

                    print(playerLabel + " has won")
                    return True

        return False

    def copy(self):
        board_copy = Board()
        board_copy.buildings = self._copy_array(self.buildings)
        board_copy.workers = self._copy_array(self.workers)
        board_copy.player1 = self.player1.copy(board_copy, 1)
        board_copy.player2 = self.player2.copy(board_copy, 2)
        return board_copy

    def _copy_array(self, array):
        array_copy = [[0 for col in range(5)] for row in range(5)]
        for i in range(5):
            for j in range(5):
                array_copy[i][j] = array[i][j]

        return array_copy
                
        