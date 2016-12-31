import boto3
import json

def get_move(game_state, configuration):
    return None


def submit_move(message, game_id, src, dest):
    pass
    # Remove message from queue


INTERVAL = 5


def main():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="CheckersOnlineAI")
    while True:
        for message in queue.receive_messages(MessageAttributeNames=['GameId', 'AIConfiguration', 'Timestamp']):
            print("message found!")
            if message.message_attributes is not None:
                game_id = message.message_attributes.get('GameId')['StringValue']
                ai_configuration = message.message_attributes.get('AIConfiguration')['StringValue']
                timestamp = message.message_attributes.get('Timestamp')['StringValue']
                print("correct attributes: {} {} {}".format(game_id, ai_configuration, timestamp))
                game_state = json.loads(message.body)
                print(game_state)
                move = get_move(game_state, ai_configuration)
                if move is not None:
                    submit_move(game_id, timestamp, move['src'], move['dest'])
            print("Deleting message")
            message.delete()
            print("Message deleted")
            # TODO: sleep INTERVAL


if __name__ == "__main__":
    main()
