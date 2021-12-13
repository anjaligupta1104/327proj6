"""
Meili and Anjali Gupta
CPSC 327 Pset
Sunday, 10:20 pm
"""

import random

from board import Board
from move import Move
class playerFactory:
    def build_player(player_type, player_num):
        if player_type == "human":
            return Human(player_num)
        if player_type == "random":
            return Random(player_num)
        if player_type == "heuristic":
            return Heuristic(player_num)

class Player:
    def __init__(self, player_num):
        self._playerNum = player_num
        if self._playerNum == 1:
            self._piece1 = [3,1]
            self._piece2 = [1,3]
        else:
            self._piece1 = [1,1]
            self._piece2 = [3,3]
    
    def choose_move(self):
        pass

    def _valid(self, piece_num, direction_letter):
        """Checks if move or build of piece in direction is out of bounds."""
        # get piece
        if piece_num == 1:
            piece = self._piece1
        else:
            piece = self._piece2

        # get direction
        directions = { #(n, ne, e, se, s, sw, w, nw)
            "n": [0,1],
            "ne": [1,1],
            "e": [1,0],
            "se": [1,-1],
            "s": [0,-1],
            "sw": [-1,-1],
            "w": [-1,0],
            "nw": [-1,1]
        }
        direction = directions.get(direction_letter)

        # check new row and column against bounds [0,4]
        new_row = piece[0] + direction[0]
        new_col = piece[1] + direction[1]

        if new_row < 0 or new_row > 4:
            return False
        elif new_col < 0 or new_col > 4:
            return False
        else:
            return True

    def enumerate_valid_moves(self):
        moves = {}
        directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
        for piece_num in range(1,2):
            for move_num in range(9):
                for build_num in range(9):
                    move = directions[move_num]
                    build = directions[build_num]
                    
                    potential_move = [piece_num, move, build]
                    if self._valid(potential_move):
                        moves.append(potential_move)
        return moves

class WorkerError(Exception):
    pass
class NotYourWorkerError(Exception):
    pass

class DirectionError(Exception):
    pass

class NonValidDirectionError(Exception):
    def __init__(self, direction):
        self.direction = direction
class Human(Player):
    def choose_move(self):
        while True:
            try:
                piece_letter = input("Select a worker to move\n")

                if piece_letter not in {'A','B','Y','Z'}:
                    raise WorkerError
                if self._playerNum == 1 and piece_letter not in {'A','B'}:
                    raise NotYourWorkerError
                if self._playerNum == 2 and piece_letter not in {'Y','Z'}:
                    raise NotYourWorkerError

                if piece_letter in {'A','Y'}: 
                    piece_num = 1
                else:
                    piece_num = 2

            except WorkerError:
                print("Not a valid worker")
            except NotYourWorkerError:
                print("That is not your worker")
            else:
                break

        while True:
            try:
                move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)")

                if move not in {"n", "ne", "e", "se", "s", "sw", "w", "nw"}:
                    raise DirectionError
                if not self._valid(piece_num, move):
                    raise NonValidDirectionError(move)

            except DirectionError:
                print("Not a valid direction")
            except NonValidDirectionError as nvd:
                print(f"Cannot move {nvd.direction}")
            else:
                break
            
        while True:
            try:
                build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)")

                if build not in {"n", "ne", "e", "se", "s", "sw", "w", "nw"}:
                    raise DirectionError
                if not self._valid(piece_num, build):
                    raise NonValidDirectionError(build)

            except DirectionError:
                print("Not a valid direction")
            except NonValidDirectionError as nvd:
                print(f"Cannot build {nvd.direction}")
            else:
                break

        return [piece_num,move,build]
class Random(Player):
    def choose_move(self):
        moves = self.enumerate_valid_moves()
        random_i = random.randint(0,len(moves)-1)
        potential_move = moves[random_i]
        return potential_move
class Heuristic(Player):
    def __init__(self):
        self.height_score = 0
        self.center_score = 0
        self.distance_score = 0
    
    def height_score(self, board):
        piece1_height = board.buildings[self._piece1[0]][self._piece1[1]]
        piece2_height = board.buildings[self._piece2[0]][self._piece2[1]]
        return piece1_height + piece2_height

    def center_score(self, board):
        piece1_center = board.buildings[self._piece1[0]]
        return 1

    def distance_score(self, board):
        return 1

    def choose_move(self):
        moves = self.enumerate_valid_moves()
        
        # weights
        c1 = 3
        c2 = 2
        c3 = 1

        # max scores
        max_height_score = 0
        max_center_score = 0
        max_distance_score = 0
        max_move_score = 0

        # iterate through all moves
        for potential_move in moves:
            my_board = Board()
            move_score = c1*self.height_score(potential_move) + c2*self.center_score(potential_move) + c3*self.distance_score(poten)
            move_scores.append(move_score)

        
            
