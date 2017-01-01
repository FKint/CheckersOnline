from ai import AICheckersState
import game_interface
from flask import Flask, request, jsonify
from flask_boto3 import Boto3
import os

application = Flask("Checkers Online AI")
if os.environ['ENVIRONMENT'] == "deployment":
    pass
else:
    application.config.from_pyfile("config/private.{}.config".format(os.environ['ENVIRONMENT']))
boto_flask = Boto3(application)


def get_move(game_state, configuration):
    state = AICheckersState(game_state['Turn'], game_state['BlackRegular'], game_state['BlackKings'],
                            game_state['WhiteRegular'], game_state['WhiteKings'], configuration)
    move = state.get_best_move(3)
    print(move)
    return move[1]


@application.route('/play-ai', methods=['POST'])
def play_ai():
    message = request.get_json()
    print("Received message: {}".format(message))
    if message.message_attributes is not None:
        game_id = message.message_attributes.get('GameId')['StringValue']
        print("playing game {}!".format(game_id))
        ai_configuration = message.message_attributes.get('AIConfiguration')['StringValue']
        timestamp = message.message_attributes.get('Timestamp')['StringValue']
        game_state = game_interface.get_current_game_state(game_id, timestamp=timestamp)
        if game_state is not None:
            move = get_move(game_state, ai_configuration)
            if move is not None and len(move) > 1:
                game_interface.execute_move(game_id, move[0], move[1:], timestamp)
            else:
                print("Didn't find a valid move: {}".format(move))
        else:
            print("Current game state timestamp does not match SQS message game state timestamp")
    return jsonify(message)


def main():
    application.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
