class Piece:
    def __init__(self, player_num, piece_num):
        self.name = self._get_name(player_num, piece_num)
        self.location = self._get_location(self.name)

    def _get_name(self, player_num, piece_num):
        """ Translates player_num and piece_num to letter name. Only to be used once at init of piece. """
        if player_num == 1:
            name = 'A' if piece_num == 1 else 'B'
        else:
            name = 'Y' if piece_num == 1 else 'Z'
        return name

    def _get_location(self, name):
        """ Translates name to initial start location. Only to be used once at init of piece. """
        start_locations = {
            'A': [3,1],
            'B': [1,3],
            'Y': [1,1],
            'Z': [3,3]
        }
        return start_locations.get(name)

    def change_location(self, x, y):
        """ Updates location index of piece object with delta x and delta y. """
        self.location[0] = self.location[0] + x
        self.location[1] = self.location[1] + y

    def copy(self, player_num, piece_num):
        piece_copy = Piece(player_num, piece_num)
        piece_copy.name = self.name
        piece_copy.location = [0,0]
        piece_copy.location[0] = self.location[0]
        piece_copy.location[1] = self.location[1]
        return piece_copy