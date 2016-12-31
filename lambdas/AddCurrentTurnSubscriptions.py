from __future__ import print_function

import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('UsersCollection')


def add_current_turn(player_id, game_id):
    if str(player_id) == str("-1"):
        return
    print("Adding the game %s as a 'current turn' subscription for player %s" % (game_id, player_id))
    users_table.update_item(
        Key={"Handle": player_id},
        UpdateExpression="ADD GamesCurrentTurn :g",
        ExpressionAttributeValues={":g": {game_id}}
    )


def remove_current_turn(player_id, game_id):
    if str(player_id) == str("-1"):
        return
    print("Removing the game %s as a 'current turn' subscription for player %s" % (game_id, player_id))
    users_table.update_item(
        Key={"Handle": player_id},
        UpdateExpression="DELETE GamesCurrentTurn :g",
        ExpressionAttributeValues={":g": {game_id}}
    )


def lambda_handler(event, context):
    for record in event['Records']:
        new_image = record['dynamodb']['NewImage']
        game_id = new_image['GameId']['S']
        white_player_id = new_image['WhitePlayerId']['S']
        black_player_id = new_image['BlackPlayerId']['S']
        if record['eventName'] == 'INSERT':
            add_current_turn(white_player_id, game_id)
        elif record['eventName'] == 'MODIFY':
            state = new_image['GameStates']['L'][-1]['M']
            winner = state['Winner']['S'] if 'S' in state['Winner'] else None
            turn = state['Turn']['S']
            current_turn = white_player_id if turn == "WHITE" else black_player_id
            previous_turn = black_player_id if turn == "WHITE" else white_player_id
            remove_current_turn(previous_turn, game_id)
            if winner is not None:
                pass
            else:
                add_current_turn(current_turn, game_id)
    return 'Successfully processed {} records.'.format(len(event['Records']))
