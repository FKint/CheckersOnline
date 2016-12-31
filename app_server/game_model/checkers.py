import json

from game_model import helpers


WHITE = "WHITE"
BLACK = "BLACK"

REGULAR = "REGULAR"
KING = "KING"


class InvalidTurnException(Exception):
    def __init__(self, message):
        self.message = message


class CheckersState:
    def __init__(self, turn, black_regular, black_kings, white_regular, white_kings):
        self.turn = turn
        self.black_regular = list(map(tuple, black_regular))
        self.white_regular = list(map(tuple, white_regular))
        self.black_kings = list(map(tuple, black_kings))
        self.white_kings = list(map(tuple, white_kings))

    def get_next_turn(self):
        return WHITE if self.turn == BLACK else BLACK

    def get_game_state_after_turn(self):
        return {
            "Winner": self.get_winner(),
            "Turn": self.get_next_turn(),
            "BlackRegular": list(map(helpers.convert_tuple_to_coordinate, self.black_regular)),
            "BlackKings": list(map(helpers.convert_tuple_to_coordinate, self.black_kings)),
            "WhiteRegular": list(map(helpers.convert_tuple_to_coordinate, self.white_regular)),
            "WhiteKings": list(map(helpers.convert_tuple_to_coordinate, self.white_kings))
        }

    def validate_move(self, src, moves):
        if self.is_empty_cell(src):
            raise InvalidTurnException("Src is empty: {} {} {}".format(json.dumps(src), json.dumps(self.white_regular),
                                                                       json.dumps(self.black_regular)))
        actor = self.get_piece_at(src)
        if actor[0] != self.turn:
            raise InvalidTurnException("Current turn: {}".format(self.turn))

        if len(moves) == 0:
            raise InvalidTurnException("No moves")
        for m in moves:
            if not self.is_empty_cell(m):
                raise InvalidTurnException("Dest is not empty")
        current_location = src
        for m in moves:
            if self.is_step(current_location, m, actor):
                if not len(moves) == 1:
                    raise InvalidTurnException("Steps can only be done as the only move")
            elif not self.is_jump(current_location, m, actor):
                raise InvalidTurnException("Invalid move")
            current_location = m

        optimal_num_killed = self.get_optimal_killing(self.turn)

        if len(moves) == 1 and self.is_step(src, moves[0], actor):
            if optimal_num_killed > 0:
                raise InvalidTurnException("Should capture some!")
            self.move_piece(src, moves[0])
        else:
            current_location = src
            killed_pieces = set()
            for m in moves:
                captured = self.get_captured_piece(current_location, m)
                if captured is None:
                    raise InvalidTurnException("Cannot capture empty cell")
                if captured[0] == self.turn:
                    raise InvalidTurnException("Cannot capture own piece")
                killed_pieces.add(captured)
                current_location = m
            if len(killed_pieces) < optimal_num_killed:
                raise InvalidTurnException("Should capture more!")
            self.move_piece(src, moves[-1])
            for captured in killed_pieces:
                self.remove_piece(captured[1])

    def is_empty_cell(self, cell):
        if not self.is_valid_location(cell):
            return False
        return tuple(cell) not in map(tuple,
                                      self.black_regular + self.black_kings + self.white_regular + self.white_kings)

    def get_piece_at(self, cell):
        if cell in self.black_regular:
            return BLACK, REGULAR
        if cell in self.black_kings:
            return BLACK, KING
        if cell in self.white_regular:
            return WHITE, REGULAR
        if cell in self.white_kings:
            return WHITE, KING
        raise Exception("No piece at cell {}".format(cell))

    def is_step(self, src, dest, piece):
        if not CheckersState.is_valid_location(dest):
            return False
        if not self.is_empty_cell(dest):
            return False
        if abs(src[0] - dest[0]) != abs(src[1] - dest[1]):
            return False
        if piece[1] == REGULAR:
            if abs(src[0] - dest[0]) != 1:
                return False
            if piece[0] == BLACK:
                if dest[0] < src[0]:
                    return False
            elif piece[0] == WHITE:
                if dest[0] > src[0]:
                    return False
        else:
            v = dest[0] - src[0], dest[1] - src[1]
            v = int(v[0] / abs(v[0])), int(v[1] / abs(v[1]))
            for s in range(1, abs(dest[0] - src[0])):
                loc = src[0] + s * v[0], src[1] + s * v[1]
                if not self.is_empty_cell(loc):
                    return False
        return True

    @classmethod
    def is_valid_location(cls, cell):
        if cell[0] < 0 or cell[1] < 0 or cell[0] > 9 or cell[1] > 9:
            return False
        if (cell[0] + cell[1]) % 2 == 0:
            return False
        return True

    def is_jump(self, src, dest, piece):
        if not CheckersState.is_valid_location(dest):
            return False
        if not self.is_empty_cell(dest):
            return False
        if abs(src[0] - dest[0]) != abs(src[1] - dest[1]):
            return False
        if piece[1] == REGULAR:
            if abs(src[0] - dest[0]) != 2:
                return False
            jumped_cell = (src[0] + dest[0]) / 2, (src[1] + dest[1]) / 2
            if self.is_empty_cell(jumped_cell):
                return False
            jumped_piece = self.get_piece_at(jumped_cell)
            if jumped_piece[0] == piece[0]:
                return False
        else:
            captured_piece = self.get_captured_piece(src, dest)
            if captured_piece is None:
                return False
            if captured_piece[0][0] == piece[0]:
                return False
        return True

    def get_captured_piece(self, src, dest):
        v = dest[0] - src[0], dest[1] - src[1]
        v = int(v[0] / abs(v[0])), int(v[1] / abs(v[1]))
        captured_piece = None
        visited_locs = []
        for s in range(1, abs(dest[0] - src[0])):
            loc = src[0] + s * v[0], src[1] + s * v[1]
            visited_locs.append(loc)
            if not self.is_empty_cell(loc):
                if captured_piece is not None:
                    return None
                captured_piece = self.get_piece_at(loc), loc
        return captured_piece

    def move_piece(self, src, dest):
        piece = self.get_piece_at(src)
        if piece[0] == BLACK:
            if piece[1] == REGULAR:
                self.black_regular.remove(src)
                if dest[0] == 9:
                    self.black_kings.append(dest)
                else:
                    self.black_regular.append(dest)
            else:
                self.black_kings.remove(src)
                self.black_kings.append(dest)
        else:
            if piece[1] == REGULAR:
                self.white_regular.remove(src)
                if dest[0] == 0:
                    self.white_kings.append(dest)
                else:
                    self.white_regular.append(dest)
            else:
                self.white_kings.remove(src)
                self.white_kings.append(dest)

    def remove_piece(self, cell):
        piece = self.get_piece_at(cell)
        if piece[0] == BLACK:
            if piece[1] == REGULAR:
                self.black_regular.remove(cell)
            else:
                self.black_kings.remove(cell)
        else:
            if piece[1] == REGULAR:
                self.white_regular.remove(cell)
            else:
                self.white_kings.remove(cell)

    def get_optimal_killing_for_piece(self, piece, location, captured=None, history=None):
        if captured is None:
            captured = set()
        if history is None:
            history = set()
        valid_captures = self.get_valid_captures(piece, location)
        best = len(captured)
        for c in valid_captures:
            captured_piece = self.get_captured_piece(location, c)
            captured_piece = captured_piece[1]
            if captured_piece in captured:
                if c in history:
                    continue
                new_history = history | {c}
                new_captured = captured
            else:
                new_history = {c}
                new_captured = captured | {captured_piece}
            self.move_piece(location, c)
            best = max(best, self.get_optimal_killing_for_piece(piece, c, new_captured, new_history))
            self.move_piece(c, location)
        return best

    regular_capture_directions = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
    all_directions_vectors = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

    def get_valid_captures(self, piece, location):
        valid_captures = []
        if piece[1] == REGULAR:
            for c in CheckersState.regular_capture_directions:
                new_loc = location[0] + c[0], location[1] + c[1]
                if self.is_jump(location, new_loc, piece):
                    valid_captures.append(new_loc)
        else:
            for d in CheckersState.all_directions_vectors:
                for j in range(2, 9):
                    new_loc = location[0] + d[0] * j, location[1] + d[1] * j
                    if self.is_jump(location, new_loc, piece):
                        valid_captures.append(new_loc)
        return valid_captures

    def get_optimal_killing(self, color):
        best = 0
        if color == BLACK:
            for r in self.black_regular:
                best = max(best, self.get_optimal_killing_for_piece((BLACK, REGULAR), r))
            for k in self.black_kings:
                best = max(best, self.get_optimal_killing_for_piece((BLACK, KING), k))
        else:
            for r in self.white_regular:
                best = max(best, self.get_optimal_killing_for_piece((WHITE, REGULAR), r))
            for k in self.white_kings:
                best = max(best, self.get_optimal_killing_for_piece((WHITE, KING), k))
        return best

    def get_winner(self):
        if not self.can_move(self.get_next_turn()):
            return self.turn
        return None

    def can_move(self, color):
        if color == BLACK:
            regular_directions = [(1, 1), (1, -1)]
            regular = self.black_regular
            kings = self.black_kings
        else:
            regular_directions = [(-1, 1), (-1, -1)]
            regular = self.white_regular
            kings = self.white_kings
        for r in regular:
            for rd in regular_directions:
                new_loc = r[0] + rd[0], r[1] + rd[1]
                if self.is_empty_cell(new_loc):
                    return True
            for rcd in CheckersState.regular_capture_directions:
                new_loc = r[0] + rcd[0], r[1] + rcd[1]
                if self.is_jump(r, new_loc, REGULAR):
                    return True
        for k in kings:
            for d in CheckersState.all_directions_vectors:
                for j in range(2, 9):
                    new_loc = k[0] + d[0] * j, k[1] + d[1] * j
                    if self.is_jump(k, new_loc, KING) or self.is_step(k, new_loc, KING):
                        return True
        return False
