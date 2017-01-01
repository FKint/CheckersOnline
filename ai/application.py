from ai import AICheckersState
import game_interface
from flask import Flask, request, jsonify
from flask_boto3 import Boto3
import os

application = Flask("Checkers Online AI")
application.config.from_pyfile("config/public.general.config")
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
    print("Playing AI!")
    message = request.get_json()
    application.logger.info("Received message: {}".format(message))
    print("Received message: {}".format(message))
    if 'GameId' not in message or 'AIConfiguration' not in message or 'Timestamp' not in message:
        return jsonify({
            "msg": "Invalid message"
        })
    game_id = message['GameId']
    ai_configuration = message['AIConfiguration']
    timestamp = message['Timestamp']
    print("playing game {}!".format(game_id))
    game_state = game_interface.get_current_game_state(game_id, timestamp=timestamp)
    if game_state is not None:
        move = get_move(game_state, ai_configuration)
        if move is not None and len(move) > 1:
            game_interface.execute_move(game_id, move[0], move[1:], timestamp)
            return jsonify({
                "msg": "Move executed",
                "move": move
            })
        else:
            print("Didn't find a valid move: {}".format(move))
            return jsonify({
                "msg": "No valid move found!"
            })
    else:
        print("Current game state timestamp does not match SQS message game state timestamp")
        return jsonify({
            "msg": "Timestamp doesn't match."
        })


def main():
    application.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
