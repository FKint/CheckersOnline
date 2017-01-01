from game_model.checkers import CheckersState, REGULAR, WHITE, BLACK, KING
from game_model import helpers

WINNING_SCORE = 10000
LOSING_SCORE = -WINNING_SCORE

KING_VALUE = 10
REGULAR_VALUE = 1


def extend_best_array(current_number, current_array, new_number, new_array):
    if current_number == new_number:
        return current_number, current_array + new_array
    elif current_number < new_number:
        return new_number, new_array
    return current_number, current_array


class AICheckersState(CheckersState):
    def __init__(self, turn, black_regular, black_kings, white_regular, white_kings, ai_configuration="NORMAL"):
        CheckersState.__init__(self, turn, black_regular, black_kings, white_regular, white_kings)
        self.ai_configuration = ai_configuration

    def clone(self):
        return AICheckersState(self.turn, self.black_regular, self.black_kings, self.white_regular, self.white_kings,
                               self.ai_configuration)

    def switch_turn(self):
        self.turn = helpers.get_other_player(self.turn)

    def get_game_state_value(self):
        white_score = len(self.white_regular) * REGULAR_VALUE + len(self.white_kings) * KING_VALUE
        black_score = len(self.black_regular) * REGULAR_VALUE + len(self.black_kings) * KING_VALUE
        if self.turn == WHITE:
            return white_score - black_score
        else:
            return black_score - white_score

    def get_all_steps(self):
        all_steps = []
        if self.turn == BLACK:
            regular_directions = CheckersState.black_regular_step_directions
            regular = self.black_regular
            kings = self.black_kings
        else:
            regular_directions = CheckersState.white_regular_step_directions
            regular = self.white_regular
            kings = self.white_kings

        for r in regular:
            for rd in regular_directions:
                new_loc = r[0] + rd[0], r[1] + rd[1]
                if self.is_step(r, new_loc, (REGULAR, self.turn)):
                    all_steps.append([r, new_loc])

        for k in kings:
            for d in CheckersState.all_directions_vectors:
                for j in range(2, 9):
                    new_loc = k[0] + d[0] * j, k[1] + d[1] * j
                    if self.is_step(k, new_loc, (KING, self.turn)):
                        all_steps.append([k, new_loc])

        return all_steps

    def get_optimal_killing_for_piece(self, piece, location, captured=None, history=None):
        #TODO: check that kings don't jump back over killed pieces
        if captured is None:
            captured = set()
        if history is None:
            history = []
        history = history[:] + [location]
        valid_captures = self.get_valid_captures(piece, location)
        best_number = len(captured)
        best_moves = [history]
        for c in valid_captures:
            captured_piece = self.get_captured_piece(location, c)
            captured_piece = captured_piece[1]
            if captured_piece in captured:
                #No captured piece can be jumped twice
                continue
                #if c in history:
                #    continue
                #new_history = history | {c}
                #new_captured = captured
            #new_history = {c}
            new_captured = captured | {captured_piece}
            self.move_piece(location, c)
            number, moves = self.get_optimal_killing_for_piece(piece, c, new_captured, history=history)
            best_number, best_moves = extend_best_array(best_number, best_moves, number, moves)
            self.move_piece(c, location)
        return best_number, best_moves

    def get_optimal_killings(self):
        best_number = 0
        best_moves = []
        if self.turn == BLACK:
            for r in list(self.black_regular):
                number, moves = self.get_optimal_killing_for_piece((BLACK, REGULAR), r)
                best_number, best_moves = extend_best_array(best_number, best_moves, number, moves)
            for k in list(self.black_kings):
                number, moves = self.get_optimal_killing_for_piece((BLACK, KING), k)
                best_number, best_moves = extend_best_array(best_number, best_moves, number, moves)
        else:
            for r in list(self.white_regular):
                number, moves = self.get_optimal_killing_for_piece((WHITE, REGULAR), r)
                best_number, best_moves = extend_best_array(best_number, best_moves, number, moves)
            for k in list(self.white_kings):
                number, moves = self.get_optimal_killing_for_piece((WHITE, KING), k)
                best_number, best_moves = extend_best_array(best_number, best_moves, number, moves)
        return best_number, best_moves

    def get_best_move(self, depth_remaining):
        if self.get_winner() == self.turn:
            return WINNING_SCORE, []
        elif self.get_winner() == helpers.get_other_player(self.turn):
            return LOSING_SCORE, []
        if depth_remaining < 0:
            return self.get_game_state_value(), []
        optimal_killings = self.get_optimal_killings()
        possible_moves = []
        if optimal_killings[0] > 0:
            possible_moves.extend(optimal_killings[1])
        else:
            possible_moves.extend(self.get_all_steps())

        best_score = LOSING_SCORE
        best_moves = []
        for pm in possible_moves:
            new_state = self.clone()
            new_state.validate_move(pm[0], pm[1:])
            new_state.switch_turn()
            score, next_move = new_state.get_best_move(depth_remaining=depth_remaining - 1)
            if depth_remaining == 5:
                print(depth_remaining, score, next_move)
            if score > best_score:
                best_moves = [pm]
                best_score = score
            elif score == best_score:
                best_moves.append(pm)
        # TODO: randomize
        return best_score, best_moves[0]
