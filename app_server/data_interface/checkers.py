def get_valid_move(state, src, dest):
    pass


WHITE = "WHITE"
BLACK = "BLACK"

REGULAR = "REGULAR"
KING = "KING"


class InvalidTurnException(Exception):
    def __init__(self, message):
        self.message = message


class CheckersState:
    def __init__(self):
        self.turn = WHITE
        self.black_regular = []
        self.white_regular = []
        self.black_kings = []
        self.white_kings = []

    def is_valid_turn(self, src, moves):
        if self.is_empty_cell(src):
            raise InvalidTurnException("Src is empty")
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
            if self.is_step(current_location, m, actor) and not len(moves) == 1:
                raise InvalidTurnException("Steps can only be done as the only move")
            if self.is_jump(current_location, m, actor):
                raise InvalidTurnException("Invalid move")
            current_location = m

        optimal_num_killed = self.get_optimal_killing(self.turn)

        if len(moves) == 1 and self.is_step(src, moves[0], self.turn):
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
                self.remove_piece(captured)

    def is_empty_cell(self, cell):
        return cell not in (self.black_regular + self.black_kings + self.white_regular + self.white_kings)

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
            v = v[0] / abs(v[0]), v[1] / abs(v[1])
            for s in range(1, abs(v[0])):
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
        v = v[0] / abs(v[0]), v[1] / abs(v[1])
        captured_piece = None
        for s in range(1, abs(v[0])):
            loc = src[0] + s * v[0], src[1] + s * v[1]
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
                new_history = set()
                new_captured = captured
            else:
                new_history = history | {c}
                new_captured = captured | {captured_piece}
            self.move_piece(location, c)
            best = max(best, self.get_optimal_killing_for_piece(piece, c, new_captured, new_history))
            self.move_piece(c, location)
        return best

    def get_valid_captures(self, piece, location):
        valid_captures = []
        if piece[1] == REGULAR:
            regular_captures = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
            for c in regular_captures:
                new_loc = location[0] + c[0], location[1] + c[1]
                if self.is_jump(location, new_loc, piece):
                    valid_captures.append(new_loc)
        else:
            directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            for d in directions:
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
