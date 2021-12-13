class Move:
    def __init__(self, board, piece, move, build): 
        self.board = board
        self._peice = piece
        self._move = move
        self._build = build

    def execute(self):
        """Execute move with piece_num, move, and build"""
        old_row = self._piece.row
        old_col = self._peice.piece.col

        self.board.buildings