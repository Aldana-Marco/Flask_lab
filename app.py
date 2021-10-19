from flask import Flask, jsonify, request

import services.player_services as player_service

app = Flask(__name__)


# endpoint

@app.route('/users', methods=['GET', 'POST'])  # users and endpoints are in plural
def post_user():  # put application's code here
    body: dict = request.get_json(force=True)
    user = player_service.create_player(body.get("name", "default"))  # POST
    return jsonify(user.to_dict())


@app.route('/users/list', methods=['GET'])
def get_users():
    user_list = player_service.get_players()
    return jsonify(user_list)


@app.route('/users/modify', methods=['PUT'])
def put_user_by_id():
    body: dict = request.get_json(force=True)
    user = player_service.update_player(body.get("id", "default"), body.get("name", "default"))  # POST
    return jsonify(user)


@app.route('/users/delete', methods=['DELETE'])
def delete_user_by_id():
    body: dict = request.get_json(force=True)
    user = player_service.delete_player(body.get("id", "default"))  # POST
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
