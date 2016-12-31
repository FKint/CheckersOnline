import boto3
import json
from ai import AICheckersState
import game_interface


def get_move(game_state, configuration):
    state = AICheckersState(game_state['Turn'], game_state['BlackRegular'], game_state['BlackKings'],
                            game_state['WhiteRegular'], game_state['WhiteKings'], configuration)
    move = state.get_best_move(5)
    print(move)
    return move[1]


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
                    game_interface.execute_move(game_id, move[0], move[1:])
            print("Deleting message")
            message.delete()
            print("Message deleted")
            # TODO: sleep INTERVAL


if __name__ == "__main__":
    main()
