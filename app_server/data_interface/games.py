import uuid

from data_interface import checkers, users
from application import boto_flask
import time


def get_your_turn_games(user_id=None):
    user = users.get_user_account(user_id=user_id, fresh=True)
    if 'GamesCurrentTurn' not in user:
        return []
    games = user['GamesCurrentTurn']
    return [get_game_data(x) for x in games]


def get_subscribed_games(user_id=None):
    user = users.get_user_account(user_id=user_id, fresh=True)
    if 'GameSubscriptions' not in user:
        return []
    games = user['GameSubscriptions']
    return [get_game_data(x) for x in games]


def get_participating_games(user_id=None):
    user = users.get_user_account(user_id=user_id, fresh=True)
    if 'GameParticipations' not in user:
        return []
    games = user['GameParticipations']
    return [get_game_data(x) for x in games]


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


def add_game_notifications(user_id, game_id):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.update_item(
        Key={
            'Handle': {"S": user_id}
        },
        UpdateExpression="ADD PlayingGames=:value1",
        ExpressionAttributeValues={
            ":value1": {"S": game_id}
        }
    )


def generate_random_game_id():
    return str(uuid.uuid4())


def create_new_game(game_name, white_user_id, black_user_id):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('GamesCollection')
    game_id = generate_random_game_id()
    item = {
        "GameId": game_id,
        "WhitePlayerId": white_user_id,
        "BlackPlayerId": black_user_id,
        "GameName": game_name,
        "GameStates": [get_default_game_state()],
        "Winner": None,
        "StateTimestamp": str(time.time())
    }
    # TODO: check for duplicate ID
    table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(GameId)"
    )
    return game_id


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
    return convert_coordinate_game_state_to_tuple(states[-1])


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
