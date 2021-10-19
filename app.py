from flask import Flask, jsonify, request

import services.player_services as player_service
from repositories import player_repository

app = Flask(__name__)


# endpoint

@app.route('/users', methods=['GET', 'POST'])  # users and endpoints are in plural
def post_user():  # put application's code here
    body: dict = request.get_json(force=True)
    user = player_service.create_player(body.get("name", "default"))  # POST
    return jsonify(user.to_dict())


@app.route('/users/list', methods=['GET'])
def get_users():
    for user in player_repository.PlayerRepository.users:
        userdict = user.to_dict()
        return jsonify(userdict)


if __name__ == '__main__':
    app.run()
