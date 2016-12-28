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
        pass

    def get_piece_at(self, cell):
        pass

    def is_step(self, src, dest, piece):
        pass

    def is_jump(self, src, dest, piece):
        # Exactly one piece of other colour
        pass

    def get_optimal_killing(self, color):
        pass

    def get_captured_piece(self, src, dest):
        pass

    def move_piece(self, src, dest):
        pass

    def remove_piece(self, cell):
        pass
