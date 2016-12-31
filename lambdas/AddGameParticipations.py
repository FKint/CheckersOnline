from __future__ import print_function

import json
import boto3

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('UsersCollection')

def add_game_participation(player_id, game_id):
    if str(player_id) == str("-1"):
        return
    print("Adding participation of player %s to game %s" % (player_id, game_id))
    users_table.update_item(
        Key={"Handle": player_id},
        UpdateExpression="ADD GameParticipations :g",
        ExpressionAttributeValues={":g": {game_id}}
    )

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            black_player_id = new_image['BlackPlayerId']
            white_player_id = new_image['WhitePlayerId']
            add_game_participation(black_player_id['S'], new_image['GameId']['S'])
            add_game_participation(white_player_id['S'], new_image['GameId']['S'])
    return 'Successfully processed {} records.'.format(len(event['Records']))
