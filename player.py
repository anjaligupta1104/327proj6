import sys
import random
from move import Move
from piece import Piece

class WorkerError(Exception):
    pass
class NotYourWorkerError(Exception):
    pass
class DirectionError(Exception):
    pass
class NonValidDirectionError(Exception):
    def __init__(self, direction):
        self.direction = direction

class playerFactory:
    def build_player(board, player_type, player_num):
        if player_type == "human":
            return Human(board, player_num)
        if player_type == "random":
            return Random(board, player_num)
        if player_type == "heuristic":
            return Heuristic(board, player_num)

class Player:
    def __init__(self, board, player_num, player_type):
        self.board = board
        self.player_num = player_num
        self.piece1 = Piece(player_num, 1)
        self.piece2 = Piece(player_num, 2)
        self._type = player_type

        self._temp_location = None # used for try_move
        
    
    def choose_move(self):
        pass

    def no_moves_exit(self, player_num):
        if (player_num == 1):
            print("blue has won")
        else:
            print("white has won")
        sys.exit(0)

    def copy(self, board_copy, player_num):
        player_copy = playerFactory.build_player(board_copy, self._type, 1)
        player_copy.board = board_copy
        player_copy.player_num = player_num
        player_copy.piece1 = self.piece1.copy(player_num, 1) 
        player_copy.piece2 = self.piece2.copy(player_num, 2)
        return player_copy

    def _enumerate_valid_moves(self):
        moves = []
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        for piece_num in range(1,3):
            for move_num in range(8):
                for build_num in range(8):
                    move_dir = directions[move_num]
                    build_dir = directions[build_num]
                    self._set_temp(piece_num)

                    if self._try_move(move_dir) and self._try_build(build_dir):
                        move = Move(self.board, self.player_num, piece_num, move_dir, build_dir)
                        moves.append(move)
        return moves

    def _set_temp(self, piece_num):
        if piece_num == 1:
            self._temp_location = [self.piece1.location[0], self.piece1.location[1]]
        else:
            self._temp_location = [self.piece2.location[0], self.piece2.location[1]]
        self._temp_workers = self.board._copy_array(self.board.workers)

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

    def _try_move(self, dir):
        move = self._get_dir(dir)
        new_x = self._temp_location[0] + move[0]
        new_y = self._temp_location[1] + move[1]
        in_bounds = new_x >= 0 and new_x <= 4 and new_y >= 0 and new_y <= 4

        if in_bounds:
            free = self.board.workers[new_x][new_y] == 0
            height_diff = self.board.buildings[new_x][new_y] - self.board.buildings[self._temp_location[0]][self._temp_location[1]] <= 1

            if free and height_diff:
                self._temp_workers[self._temp_location[0]][self._temp_location[1]] = 0
                self._temp_location = [new_x, new_y]
                return True
            else:
                return False
        else:
            return False

    def _try_build(self, dir):
        build = self._get_dir(dir)
        build_x = self._temp_location[0] + build[0]
        build_y = self._temp_location[1] + build[1]
        in_bounds = build_x >= 0 and build_x <= 4 and build_y >= 0 and build_y <= 4

        if in_bounds:
            height_4 = self.board.buildings[build_x][build_y] < 4
            free = self._temp_workers[build_x][build_y] == 0

            return height_4 and free
        else:
            return False

    def _height_score(self):
        piece1_height = self.board.buildings[self.piece1.location[0]][self.piece1.location[1]]
        piece2_height = self.board.buildings[self.piece2.location[0]][self.piece2.location[1]]
        return piece1_height + piece2_height

    def _center_score(self):
        piece1_center = self._center_helper(self.piece1.location[0], self.piece1.location[1])
        piece2_center = self._center_helper(self.piece2.location[0], self.piece2.location[1])
        return piece1_center + piece2_center

    def _center_helper(self, x, y):
        if x == 2 and y == 2:
            return 2
        elif x >= 1 and x <= 3 and y >= 1 and y <= 3:
            return 1
        else:
            return 0

    def _distance_score(self):
        otherPlayer = self.board.player2 if self.player_num == 1 else self.board.player1 
        distance_other1 = min(self._distance_helper(self.piece1, otherPlayer.piece1), self._distance_helper(self.piece2, otherPlayer.piece1))
        distance_other2 = min(self._distance_helper(self.piece1, otherPlayer.piece2), self._distance_helper(self.piece2, otherPlayer.piece2))
        return 8 - (distance_other1 + distance_other2)
        
    def _distance_helper(self, piece1, piece2):
        distance_x = abs(piece1.location[0] - piece2.location[0])
        distance_y = abs(piece1.location[1] - piece2.location[1])

        return abs(distance_x - distance_y) + min(distance_x,distance_y)

    def _move_score(self):
        height_score = self._height_score()
        center_score = self._center_score()
        distance_score = self._distance_score()
        move_score = 3*height_score + 2*center_score + 1*distance_score
        return (move_score, height_score, center_score, distance_score)

class Human(Player):
    def __init__(self, board, player_num, player_type = "human"):
        super().__init__(board, player_num, player_type)

    def choose_move(self):
        moves = self._enumerate_valid_moves()
        if not moves:
            self.no_moves_exit(self.player_num)

        while True:
            try:
                piece_letter = input("Select a worker to move\n")

                if piece_letter not in {'A','B','Y','Z'}:
                    raise WorkerError
                if self.player_num == 1 and piece_letter not in {'A','B'}:
                    raise NotYourWorkerError
                if self.player_num == 2 and piece_letter not in {'Y','Z'}:
                    raise NotYourWorkerError

                piece_num = 1 if piece_letter in {'A','Y'} else 2
                self._set_temp(piece_num)

            except WorkerError:
                print("Not a valid worker")
            except NotYourWorkerError:
                print("That is not your worker")
            else:
                break

        while True:
            try:
                move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")

                if move_dir not in {"n", "ne", "e", "se", "s", "sw", "w", "nw"}:
                    raise DirectionError
                if not self._try_move(move_dir):
                    raise NonValidDirectionError(move_dir)

            except DirectionError:
                print("Not a valid direction")
            except NonValidDirectionError as nvd:
                print(f"Cannot move {nvd.direction}")
            else:
                break
            
        while True:
            try:
                build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")

                if build_dir not in {"n", "ne", "e", "se", "s", "sw", "w", "nw"}:
                    raise DirectionError

                if not self._try_build(build_dir):
                    raise NonValidDirectionError(build_dir)
            except DirectionError:
                print("Not a valid direction")
            except NonValidDirectionError as nvd:
                print(f"Cannot build {nvd.direction}")
            else:
                break

        return Move(self.board, self.player_num, piece_num, move_dir, build_dir)

class Random(Player):
    def __init__(self, board, player_num, player_type = "random"):
        super().__init__(board, player_num, player_type)

    def choose_move(self):
        moves = self._enumerate_valid_moves()
        if not moves:
            self.no_moves_exit(self.player_num)

        random_i = random.randint(0,len(moves)-1)
        move = moves[random_i]
        move.print_move()
        return move

class Heuristic(Player):
    def __init__(self, board, player_num, player_type = "heuristic"):
        super().__init__(board, player_num, player_type)
        self.height_score = 0
        self.center_score = 0
        self.distance_score = 0

    def choose_move(self):
        moves = self._enumerate_valid_moves()
        if not moves:
            self.no_moves_exit(self.player_num)

        max_move_score = 0
        max_move = None

        # iterate through all moves
        for move in moves:
            move.execute()

            (move_score, height_score, center_score, distance_score) = self._move_score()

            if move.moved_to_3():
                move_score = float('inf')
            
            if move_score > max_move_score:
                max_move = move
                max_move_score = move_score
                self.height_score = height_score
                self.center_score = center_score
                self.distance_score = distance_score
                
            move.undo()

        max_move.print_move()
        return max_move
            
        

        
            
