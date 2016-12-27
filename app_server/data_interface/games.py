import uuid

from main import boto_flask


def get_your_turn_games(handle):
    # TODO: store this information on the user record
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.get_item(Key={
        'Handle': handle
    })
    if 'Item' not in response:
        return None
    user = response['Item']
    if 'GamesCurrentTurn' in user:
        return user['GamesCurrentTurn']
    return []


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
        "WhiteKings": []
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
    print(response)


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
        "GameStates": [get_default_game_state()]
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
