from flask import Flask, jsonify, request

import services.player_services as player_service
from domain.constants import GET, POST, PUT, DELETE

app = Flask(__name__)


def _post_user():  # put application's code here
    body: dict = request.get_json()
    user = player_service.create_player(body.get("name", "default"))  # POST
    return jsonify(user.to_dict())


def _get_users():
    body: dict = request.get_json()
    if body.get("id", "default") == "default":
        app.logger.info("Executing GET list of users")
        user_list = player_service.get_players()
        return jsonify(user_list)
    else:
        app.logger.info("Executing GET list of users")
        user = player_service.get_player_by_id(body.get("id", "default"))  # POST
        return jsonify(user["name"])


def _put_user_by_id():
    body: dict = request.get_json()
    user = player_service.update_player(body.get("id", "default"), body.get("name", "default"))  # POST
    return jsonify(user)


def _delete_user_by_id():
    body: dict = request.get_json()
    user = player_service.delete_player(body.get("id", "default"))  # POST
    return jsonify(user)

# endpoint
@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])  # users and endpoints are in plural
def handle_users():
    if request.method == POST:
        return _post_user()
    elif request.method == GET:
        return _get_users()
    elif request.method == PUT:
        return _put_user_by_id()
    elif request.method == DELETE:
        return _delete_user_by_id()
    else:
        return jsonify({"Invalid Method"})


if __name__ == '__main__':
    app.run(debug=True)
