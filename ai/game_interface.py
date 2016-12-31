from game_model import checkers, helpers


def execute_move(game_id, src, dest):
    db_game_state = get_current_game_state(game_id)
    timestamp = db_game_state['Timestamp'] if 'Timestamp' in db_game_state else None
    checkers_state = checkers.CheckersState(db_game_state['Turn'], db_game_state['BlackRegular'],
                                            db_game_state['BlackKings'],
                                            db_game_state['WhiteRegular'], db_game_state['WhiteKings'])
    checkers_state.validate_move(tuple(src), list(map(tuple, dest)))
    new_db_game_state = checkers_state.get_game_state_after_turn()
    update_game_state(game_id, new_db_game_state, timestamp=timestamp)




def get_game_data(game_id):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('GamesCollection')
    response = table.get_item(
        Key={
            "GameId": game_id
        }
    )
    return response['Item']


def get_current_game_state(game_id):
    game_data = get_game_data(game_id)
    states = game_data['GameStates']
    return helpers.convert_coordinate_game_state_to_tuple(states[-1])


def update_game_state(game_id, game_state, timestamp=None):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('GamesCollection')
    winner = None
    if 'Winner' in game_state:
        winner = game_state['Winner']
    winner_update_expression = ""
    if winner == checkers.BLACK:
        winner_update_expression = ", Winner = BlackPlayerId"
    elif winner == checkers.WHITE:
        winner_update_expression = ", Winner = WhitePlayerId"
    expression_attribute_values = {
        ":s": [game_state],
        ":t1": str(time.time())
    }
    condition_expression = "attribute_exists(GameId)"
    if timestamp is not None:
        expression_attribute_values[':t0'] = timestamp
        condition_expression = "StateTimestamp = :t0"
    response = table.update_item(
        Key={
            "GameId": game_id
        },
        UpdateExpression="SET GameStates = list_append(GameStates, :s), StateTimestamp = :t1" + winner_update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression,
    )
