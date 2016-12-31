import boto3
import json
import time

from game_model.helpers import get_default_game_state

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='CheckersOnlineAI')

new_game = get_default_game_state()
# Create a new message
response = queue.send_message(
    MessageBody=json.dumps(new_game),
    MessageAttributes={
        "GameId": {
            "StringValue": "0000",
            "DataType": "String"
        },
        "AIConfiguration": {
            "StringValue": "NORMAL",
            "DataType": "String"
        },
        "Timestamp": {
            "StringValue": str(time.time()),
            "DataType": "String"
        }
    })

# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))
