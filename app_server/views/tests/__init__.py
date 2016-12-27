import datetime

import requests
from flask import jsonify

from main import app, boto_flask


@app.route('/tests/ai')
def test_ai():
    r = requests.get('http://ai:5000/')
    return jsonify(r.json())


@app.route('/tests/boto3')
def test_boto3():
    return jsonify(str(boto_flask.clients))


@app.route('/tests/boto3/dynamodb')
def test_dynamodb():
    return jsonify(str(boto_flask.clients['dynamodb'].list_tables()))


@app.route('/tests/boto3/dynamodb/users')
def test_dynamodb_users():
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.scan()
    return jsonify(response['Items'])


@app.route('/tests/boto3/dynamodb/games')
def test_dynamodb_games():
    dynamodb1 = boto_flask.clients['dynamodb']
    response1 = dynamodb1.describe_table(
        TableName="GamesCollection"
    )
    dynamodb2 = boto_flask.resources['dynamodb']
    table = dynamodb2.Table('GamesCollection')
    response2 = table.scan()
    return jsonify({"description": response1["Table"], "content": response2})


@app.route('/tests/boto3/dynamodb/create/games')
def test_create_games_dynamodb():
    client = boto_flask.clients['dynamodb']
    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'GameId',
                'AttributeType': 'S'
            },
        ],
        TableName='GamesCollection',
        KeySchema=[
            {
                'AttributeName': 'GameId',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return jsonify(response)


@app.route('/tests/boto3/dynamodb/create/users')
def test_create_users_dynamodb():
    client = boto_flask.clients['dynamodb']
    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': "Handle",
                'AttributeType': "S"
            }, {
                'AttributeName': "Email",
                'AttributeType': "S"
            }
        ],
        TableName='UsersCollection',
        KeySchema=[{
            "AttributeName": "Handle",
            "KeyType": "HASH"
        }],
        GlobalSecondaryIndexes=[{
            "IndexName": "UsersByEmail",
            "KeySchema": [
                {
                    "AttributeName": "Email",
                    "KeyType": "HASH"
                }
            ],
            "Projection": {
                "ProjectionType": "ALL"
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    return jsonify(response)


@app.route('/tests/boto3/dynamodb/games/insert')
def test_insert_game_dynamodb():
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('GamesCollection')
    response = table.put_item(
        Item={
            "GameId": "test-game-id",
            "Timestamp": str(datetime.datetime.now())
        }
    )
    return jsonify(response)
