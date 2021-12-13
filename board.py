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
        