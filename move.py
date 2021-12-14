class Move:
    def __init__(self, board, player_num, piece_num, move_dir, build_dir): 
        self.board = board
        self._piece = self._get_piece(board, player_num, piece_num)
        self._move = self._get_dir(move_dir)
        self._build = self._get_dir(build_dir)

        self._move_dir = move_dir
        self._build_dir = build_dir

    def _get_piece(self, board, player_num, piece_num):
        """ Returns piece from player_num and piece_num. Ex. get_piece(1,1) returns board.player1.piece1 """
        if player_num == 1:
            if piece_num == 1:
                piece = board.player1.piece1
            else:
                piece = board.player1.piece2
        else:
            if piece_num == 1:
                piece = board.player2.piece1
            else:
                piece = board.player2.piece2

        return piece

    def execute(self):
        """ Execute move with piece_num, move, and build """
        # update piece location
        self.board.workers[self._piece.location[0]][self._piece.location[1]] = 0
        self._piece.change_location(self._move[0], self._move[1])

        # update workers
        self.board.workers[self._piece.location[0]][self._piece.location[1]] = self._piece.name

        # update buildings
        build_x = self._piece.location[0] + self._build[0]
        build_y = self._piece.location[1] + self._build[1]
        self.board.buildings[build_x][build_y] += 1

    def undo(self):
        """ Does the opposite of execute. """

        # reverse piece location
        old_piece_x = self._piece.location[0]
        old_piece_y = self._piece.location[1]
        self._piece.change_location(-1 * self._move[0], -1 * self._move[1])

        # reverse workers
        self.board.workers[old_piece_x][old_piece_y] = 0
        self.board.workers[self._piece.location[0]][self._piece.location[1]] = self._piece.name

        # reverse buildings
        build_x = old_piece_x + self._build[0]
        build_y = old_piece_y + self._build[1]
        self.board.buildings[build_x][build_y] -= 1

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

    def print_move(self):
        """ Used for random to print piece.name, move_dir, and build_dir"""
        print(self._piece.name + "," + self._move_dir + "," + self._build_dir)

    def moved_to_3(self):
        return self.board.buildings[self._piece.location[0]][self._piece.location[1]] == 3