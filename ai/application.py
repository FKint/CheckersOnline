import boto3
import json
from ai import AICheckersState
import game_interface
from game_model import helpers

import time


def get_move(game_state, configuration):
    state = AICheckersState(game_state['Turn'], game_state['BlackRegular'], game_state['BlackKings'],
                            game_state['WhiteRegular'], game_state['WhiteKings'], configuration)
    move = state.get_best_move(3)
    print(move)
    return move[1]


INTERVAL = 5


def main():
    print("Starting AI worker")
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="CheckersOnlineAI")
    while True:
        print("Receiving queue messages")
        for message in queue.receive_messages(MessageAttributeNames=['GameId', 'AIConfiguration', 'Timestamp']):
            print("Found message")
            if message.message_attributes is not None:
                game_id = message.message_attributes.get('GameId')['StringValue']
                print("playing game {}!".format(game_id))
                ai_configuration = message.message_attributes.get('AIConfiguration')['StringValue']
                timestamp = message.message_attributes.get('Timestamp')['StringValue']
                game_state = json.loads(message.body)
                game_state = helpers.convert_sqs_coordinate_game_state_to_tuple(game_state)
                move = get_move(game_state, ai_configuration)
                if move is not None:
                    game_interface.execute_move(game_id, move[0], move[1:])
            message.delete()
            print("Message deleted")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
