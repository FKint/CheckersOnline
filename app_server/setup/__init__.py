from application import app, boto_flask
import click
import json

@app.cli.command()
def create_users_table():
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
    return click.echo(json.dumps(response))


@app.cli.command()
def create_games_table():
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
    return click.echo(json.dumps(response))


@app.cli.command()
def init_dynamodb():
    click.echo("Creating users table...")
    create_users_table()
    click.echo("Creating games table...")
    create_games_table()
    click.echo("Done.")


@app.cli.command()
def test_cli():
    click.echo("Testing CLI...")
