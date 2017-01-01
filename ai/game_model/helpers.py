from game_model import checkers


def convert_tuple_to_coordinate(t):
    return "{}-{}".format(t[0], t[1])


def convert_coordinate_to_tuple(c):
    r, c = c.split('-')
    return int(r), int(c)


def convert_coordinate_game_state_to_tuple(game_state):
    return {
        "BlackRegular": list(map(convert_coordinate_to_tuple, game_state['BlackRegular'])),
        "WhiteRegular": list(map(convert_coordinate_to_tuple, game_state['WhiteRegular'])),
        "BlackKings": list(map(convert_coordinate_to_tuple, game_state['BlackKings'])),
        "WhiteKings": list(map(convert_coordinate_to_tuple, game_state['WhiteKings'])),
        "Turn": game_state['Turn'],
        "Winner": game_state['Winner'] if 'Winner' in game_state else None
    }


def convert_sqs_coordinate_to_tuple(c):
    return convert_coordinate_to_tuple(c['S'])


def convert_sqs_coordinate_game_state_to_tuple(game_state):
    return {
        "BlackRegular": list(map(convert_sqs_coordinate_to_tuple, game_state['BlackRegular']['L'])),
        "BlackKings": list(map(convert_sqs_coordinate_to_tuple, game_state['BlackKings']['L'])),
        "WhiteRegular": list(map(convert_sqs_coordinate_to_tuple, game_state['WhiteRegular']['L'])),
        "WhiteKings": list(map(convert_sqs_coordinate_to_tuple, game_state['WhiteKings']['L'])),
        "Turn": game_state['Turn']['S'],
        "Winner": game_state['Winner']['S'] if 'winner' in game_state else None
    }


def get_default_game_state():
    black_regular = []
    white_regular = []
    for i in range(4):
        black_regular.extend(
            [(i, (i + 1) % 2 + 2 * j) for j in range(5)]
        )
        white_regular.extend(
            [(9 - i, i % 2 + 2 * j) for j in range(5)]
        )
    return {
        "BlackRegular": list(map(convert_tuple_to_coordinate, black_regular)),
        "BlackKings": [],
        "WhiteRegular": list(map(convert_tuple_to_coordinate, white_regular)),
        "WhiteKings": [],
        "Turn": checkers.WHITE
    }


def get_other_player(color):
    return "WHITE" if color == "BLACK" else "BLACK"
