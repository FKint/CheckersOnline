def get_next_game():
    message = None
    return message


def get_game_id(message):
    game_id = None
    return game_id


def get_game_state(game_id):
    return None


def get_ai_configuration(message):
    pass


def is_ai_turn(game_state):
    pass


def remove_message(message):
    pass


def get_move(game_state, configuration):
    return None


def submit_move(message, game_id, src, dest):
    pass
    # Remove message from queue


def main():
    while True:
        game_to_play_message = None
        while game_to_play_message is None:
            game_to_play_message = get_next_game()
            if game_to_play_message is None:
                # TODO: sleep INTERVAL
                pass
        game_id = get_game_id(game_to_play_message)
        game_state = get_game_state(game_id)
        if not is_ai_turn(game_state):
            remove_message(game_to_play_message)
            continue
        ai_configuration = get_ai_configuration(game_to_play_message)
        move = get_move(game_state, ai_configuration)
        submit_move(game_to_play_message, game_id, move['src'], move['dest'])


if __name__ == "__main__":
    main()
