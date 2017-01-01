import unittest
from game_model import checkers


class TestCheckersState(unittest.TestCase):
    def test_immutable_get_optimal_killing_number(self):
        state = checkers.CheckersState(
            turn=checkers.WHITE,
            white_regular=[(9, 2), (9, 4), (9, 6), (9, 8), (8, 5), (8, 7), (8, 9), (7, 0),
                           (7, 6), (6, 9), (4, 9), (5, 8), (8, 1), (4, 5), (7, 4), (5, 4)],
            white_kings=[],
            black_regular=[(0, 3), (0, 7), (0, 9), (1, 2), (1, 6), (1, 8), (2, 9), (3, 8),
                           (3, 0), (3, 2), (2, 5), (1, 4), (3, 6)],
            black_kings=[])
        src = (4, 5)
        dest = [(2, 7), (0, 5), (2, 3), (0, 1)]

        state.validate_move(src, dest)
        self.assertEqual(1, len(state.white_kings))

    def test_switch_turn(self):
        state = checkers.CheckersState(checkers.WHITE, [], [], [], [])
        state.switch_turn()
        self.assertEqual(checkers.BLACK, state.turn)
        state.switch_turn()
        self.assertEqual(checkers.WHITE, state.turn)
