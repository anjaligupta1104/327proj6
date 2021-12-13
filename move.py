class Move:
    def __init__(self, board, player_num, piece_num, move, build): 
        self.board = board
        self._piece = self._get_piece(player_num, piece_num)
        self._move = move
        self._build = build

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
        old_piece = self._piece.location
        self._piece.change_location(self._move[0], self._move[1])

        # update workers
        self.board.workers[old_piece[0]][old_piece[1]] = 0
        self.board.workers[self._piece.location[0]][self._piece.location[1]] = self._piece.name

        # update buildings
        build_x = self._piece.location[0] + self._build[0]
        build_y = self._piece.location[1] + self._build[1]
        self.board.buildings[build_x][build_y] += 1

    def undo(self):
        """ Does the opposite of execute. """
        reverse_move = -1 * self._move

        # reverse piece location
        old_piece = self._piece.location
        self._piece.change_location(reverse_move[0], reverse_move[1])

        # reverse workers
        self.board.workers[old_piece[0]][old_piece[1]] = 0
        self.board.workers[self._piece.location[0]][self._piece.location[1]] = self._piece.name

        # reverse buildings
        build_x = old_piece[0] + self._build[0]
        build_y = old_piece[1] + self._build[1]
        self.board.buildings[build_x][build_y] -= 1