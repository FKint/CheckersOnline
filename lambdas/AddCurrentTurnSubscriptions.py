from __future__ import print_function

import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('UsersCollection')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='CheckersOnlineAI')


def add_current_turn(player_id, game_id, game_state, timestamp):
    if str(player_id) == str("-1"):
        print("Adding an AI subscription for game %s" % game_id)
        response = queue.send_message(
            MessageBody=json.dumps(game_state),
            MessageAttributes={
                "GameId": {
                    "StringValue": game_id,
                    "DataType": "String"
                },
                "AIConfiguration": {
                    "StringValue": "NORMAL",
                    "DataType": "String"
                },
                "Timestamp": {
                    "StringValue": timestamp,
                    "DataType": "String"
                }
            })
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
        timestamp = new_image['StateTimestamp']['S'] if 'StateTimestamp' in new_image else None
        state = new_image['GameStates']['L'][-1]['M']
        if record['eventName'] == 'INSERT':
            add_current_turn(white_player_id, game_id, state, timestamp)
        elif record['eventName'] == 'MODIFY':
            winner = state['Winner']['S'] if 'S' in state['Winner'] else None
            turn = state['Turn']['S']
            current_turn = white_player_id if turn == "WHITE" else black_player_id
            previous_turn = black_player_id if turn == "WHITE" else white_player_id
            remove_current_turn(previous_turn, game_id)
            if winner is not None:
                pass
            else:
                add_current_turn(current_turn, game_id, state, timestamp)
    return 'Successfully processed {} records.'.format(len(event['Records']))
