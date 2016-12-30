import datetime

import requests
from flask import jsonify

from application import app, boto_flask


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


def convert_user_friends_sets_to_lists(elements):
    for el in elements:
        if 'Friends' in el:
            el['Friends'] = list(el['Friends'])


@app.route('/tests/boto3/dynamodb/users')
def test_dynamodb_users():
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.scan()
    items = response['Items']
    convert_user_friends_sets_to_lists(items)
    return jsonify(items)


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
